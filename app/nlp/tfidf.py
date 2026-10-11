import math
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set, Optional
from app.nlp.tokenizer import tokenize

class TFIDFEngine:
    def __init__(self):
        self._doc_tokens: Dict[int, List[str]] = {}
        self._doc_tags: Dict[int, Set[str]] = {}
        self._doc_titles: Dict[int, str] = {}
        self._idf: Dict[str, float] = {}
        self._tf_idf_vectors: Dict[int, Dict[str, float]] = {}
        self._vector_norms: Dict[int, float] = {}
        self._is_stale: bool = True

    def invalidate(self) -> None:
        """Mark index as needing rebuild."""
        self._is_stale = True

    def build_index(
        self,
        documents: List[Dict[str, any]],  # list of {"id": int, "title": str, "content": str, "tags": List[str]}
    ) -> None:
        """Rebuild in-memory TF-IDF index across all documents."""
        self._doc_tokens.clear()
        self._doc_tags.clear()
        self._doc_titles.clear()
        self._tf_idf_vectors.clear()
        self._vector_norms.clear()
        self._idf.clear()

        doc_count = len(documents)
        if doc_count == 0:
            self._is_stale = False
            return

        doc_freq = defaultdict(int)

        for doc in documents:
            doc_id = doc["id"]
            title = doc.get("title", "")
            content = doc.get("content", "") or ""
            tags = doc.get("tags", [])

            # Tokens from title (weighted x2) and content
            title_tokens = tokenize(title, remove_stopwords=True, stem=True)
            content_tokens = tokenize(content, remove_stopwords=True, stem=True)
            all_tokens = title_tokens + title_tokens + content_tokens

            self._doc_tokens[doc_id] = all_tokens
            self._doc_tags[doc_id] = {t.lower() for t in tags}
            self._doc_titles[doc_id] = title

            unique_terms = set(all_tokens)
            for term in unique_terms:
                doc_freq[term] += 1

        # Compute IDF with smoothing
        for term, df in doc_freq.items():
            self._idf[term] = math.log((1.0 + doc_count) / (1.0 + df)) + 1.0

        # Compute TF-IDF vectors & Euclidean norms
        for doc_id, tokens in self._doc_tokens.items():
            if not tokens:
                self._tf_idf_vectors[doc_id] = {}
                self._vector_norms[doc_id] = 0.0
                continue

            tf_counts = Counter(tokens)
            total_tokens = len(tokens)
            vector = {}
            norm_sq = 0.0

            for term, count in tf_counts.items():
                tf = count / total_tokens
                tfidf = tf * self._idf.get(term, 1.0)
                vector[term] = tfidf
                norm_sq += tfidf * tfidf

            self._tf_idf_vectors[doc_id] = vector
            self._vector_norms[doc_id] = math.sqrt(norm_sq)

        self._is_stale = False

    def cosine_similarity(self, doc_id_1: int, doc_id_2: int) -> float:
        """Compute cosine similarity between two indexed documents."""
        v1 = self._tf_idf_vectors.get(doc_id_1, {})
        v2 = self._tf_idf_vectors.get(doc_id_2, {})
        norm1 = self._vector_norms.get(doc_id_1, 0.0)
        norm2 = self._vector_norms.get(doc_id_2, 0.0)

        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0

        # Dot product
        # Iterate through smaller vector for speed
        if len(v1) > len(v2):
            v1, v2 = v2, v1

        dot_product = sum(weight * v2.get(term, 0.0) for term, weight in v1.items())
        return dot_product / (norm1 * norm2)

    def get_related_notes(
        self,
        target_note_id: int,
        exclude_note_ids: Optional[Set[int]] = None,
        tag_boost_weight: float = 0.2,
        limit: int = 5,
    ) -> List[Tuple[int, float]]:
        """
        Find top related notes using TF-IDF cosine similarity + shared-tag boost.
        Returns list of (note_id, combined_score).
        """
        if target_note_id not in self._tf_idf_vectors:
            return []

        exclude = exclude_note_ids or set()
        exclude.add(target_note_id)

        target_tags = self._doc_tags.get(target_note_id, set())
        results = []

        for other_id in self._tf_idf_vectors:
            if other_id in exclude:
                continue

            tfidf_sim = self.cosine_similarity(target_note_id, other_id)
            other_tags = self._doc_tags.get(other_id, set())

            # Shared tags boost
            shared_tags_count = len(target_tags.intersection(other_tags))
            tag_boost = min(0.5, shared_tags_count * tag_boost_weight)

            score = (tfidf_sim * 0.7) + (tag_boost * 0.3)
            if score > 0.01:
                results.append((other_id, round(score, 4)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

    def extract_top_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract top TF-IDF keywords from raw text."""
        tokens = tokenize(text, remove_stopwords=True, stem=False)
        if not tokens:
            return []

        counts = Counter(tokens)
        total = len(tokens)
        scored_terms = []

        for term, count in counts.items():
            tf = count / total
            stemmed = tokenize(term, remove_stopwords=False, stem=True)
            stem_key = stemmed[0] if stemmed else term
            idf = self._idf.get(stem_key, 1.5)
            scored_terms.append((term, tf * idf))

        scored_terms.sort(key=lambda x: x[1], reverse=True)
        return [term for term, _ in scored_terms[:top_k]]

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity directly between two raw text strings."""
        tokens1 = tokenize(text1, remove_stopwords=True, stem=True)
        tokens2 = tokenize(text2, remove_stopwords=True, stem=True)
        if not tokens1 or not tokens2:
            return 0.0

        c1 = Counter(tokens1)
        c2 = Counter(tokens2)
        len1 = len(tokens1)
        len2 = len(tokens2)

        v1 = {term: (count / len1) * self._idf.get(term, 1.5) for term, count in c1.items()}
        v2 = {term: (count / len2) * self._idf.get(term, 1.5) for term, count in c2.items()}

        norm1 = math.sqrt(sum(w * w for w in v1.values()))
        norm2 = math.sqrt(sum(w * w for w in v2.values()))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0

        if len(v1) > len(v2):
            v1, v2 = v2, v1

        dot = sum(w * v2.get(t, 0.0) for t, w in v1.items())
        return round(dot / (norm1 * norm2), 4)

tfidf_engine = TFIDFEngine()

