import re
from typing import List, Dict, Any, Set, Tuple, Optional
from app.assist.provider import AssistProvider
from app.nlp.tag_intelligence import (
    normalize_tag,
    parse_raw_tag_string,
    detect_phrase_merges,
    detect_tag_typos,
)
from app.nlp.proofreader import proofreader
from app.nlp.tag_suggester import suggest_tags
from app.nlp.tfidf import tfidf_engine

class RuleBasedProvider(AssistProvider):
    """
    Default offline, deterministic provider using classic NLP rules
    and local IR heuristics. Never makes external network or LLM calls.
    """

    def suggest_tags(
        self,
        title: str,
        content: str,
        current_tags: List[str],
        existing_tags: List[str],
        corpus_bigrams: Set[Tuple[str, str]],
    ) -> Dict[str, Any]:
        # 1. Normalize current tags
        normalized_tags: List[str] = []
        seen = set()
        for t in current_tags:
            norm = normalize_tag(t)
            if norm and norm not in seen:
                seen.add(norm)
                normalized_tags.append(norm)

        # 2. Phrase merges
        full_text = f"{title or ''} {content or ''}"
        merges = detect_phrase_merges(
            tags=normalized_tags,
            context_text=full_text,
            existing_tags=existing_tags,
            corpus_bigrams=corpus_bigrams,
        )

        # 3. Typo corrections
        corrections = detect_tag_typos(
            tags=normalized_tags,
            existing_tags=existing_tags,
        )

        # 4. Keyword suggestions (from note content keywords and existing tags)
        suggestions: List[Dict[str, str]] = []
        suggested_seen = set(normalized_tags)

        # Top keywords from note content
        if full_text.strip():
            top_kws = tfidf_engine.extract_top_keywords(full_text, top_k=6)
            for kw in top_kws:
                norm_kw = normalize_tag(kw)
                if norm_kw and norm_kw not in suggested_seen:
                    suggested_seen.add(norm_kw)
                    suggestions.append({
                        "tag": norm_kw,
                        "reason": "Derived from note keywords",
                    })

        # Suggestions from existing tags
        tags_with_counts = [(t, 1) for t in existing_tags]
        existing_scored = suggest_tags(
            query="",
            selected_tags=normalized_tags,
            all_tags_with_counts=tags_with_counts,
            tag_co_occurrences={},
            note_content=full_text,
            limit=6,
        )
        for s in existing_scored:
            if s["name"] not in suggested_seen:
                suggested_seen.add(s["name"])
                suggestions.append({
                    "tag": s["name"],
                    "reason": "Existing tag in graph",
                })

        return {
            "normalized": normalized_tags,
            "suggestions": suggestions,
            "merges": merges,
            "corrections": corrections,
        }

    def proofread(
        self,
        text: str,
        known_titles: List[str],
        known_tags: List[str],
        ignored_words: List[str],
    ) -> List[Dict[str, Any]]:
        return proofreader.proofread(
            text=text,
            known_titles=known_titles,
            known_tags=known_tags,
            ignored_words=ignored_words,
        )

    def suggest_links(
        self,
        note_id: int,
        note_title: str,
        note_content: str,
        note_tags: List[str],
        candidates: List[Dict[str, Any]],
        dismissed_ids: Set[int],
    ) -> List[Dict[str, Any]]:
        results = []
        note_text = f"{note_title or ''}\n{note_content or ''}".lower()
        note_tags_set = {t.lower() for t in note_tags}

        for cand in candidates:
            cand_id = cand["id"]
            if cand_id == note_id or cand_id in dismissed_ids:
                continue

            if cand.get("already_linked"):
                continue

            cand_title = cand["title"]
            cand_tags = {t.lower() for t in cand.get("tags", [])}
            cand_content = cand.get("content", "")

            score = 0.0
            reasons = []

            # Signal (a): Whole-word case-insensitive mention of candidate title or main title keywords
            escaped_title = re.escape(cand_title.lower())
            if re.search(r"\b" + escaped_title + r"\b", note_text):
                score += 0.65
                reasons.append(f"mentions '{cand_title}'")
            else:
                # Check for significant title keywords (length >= 4, ignoring common generic suffix words)
                cand_title_words = [
                    w for w in re.findall(r"\b[a-zA-Z]{4,}\b", cand_title.lower())
                    if w not in {"note", "notes", "guide", "info", "overview", "part", "intro"}
                ]
                for tw in cand_title_words:
                    if re.search(r"\b" + re.escape(tw) + r"\b", note_text):
                        score += 0.50
                        reasons.append(f"mentions '{cand_title}'")
                        break

            # Signal (b): TF-IDF similarity between notes
            tfidf_sim = tfidf_engine.calculate_similarity(
                f"{note_title} {note_content}",
                f"{cand_title} {cand_content}",
            )
            if tfidf_sim >= 0.15:
                score += min(0.35, tfidf_sim * 0.5)
                reasons.append("similar content (TF-IDF)")

            # Signal (c): Shared tags
            shared_tags = note_tags_set.intersection(cand_tags)
            if shared_tags:
                tag_boost = len(shared_tags) * 0.20
                score += min(0.35, tag_boost)
                reasons.append(f"shared tags: {', '.join(sorted(shared_tags))}")

            # Signal (d): Shared / mutual neighbours
            shared_neighbours = cand.get("shared_neighbours", [])
            if shared_neighbours:
                neigh_boost = len(shared_neighbours) * 0.10
                score += min(0.20, neigh_boost)
                reasons.append(f"shared connection with '{shared_neighbours[0]}'")

            # Minimum score threshold to avoid noisy links
            if score >= 0.20 and reasons:
                results.append({
                    "note_id": cand_id,
                    "title": cand_title,
                    "score": round(score, 3),
                    "reasons": reasons,
                })

        # Sort by score descending and return top 5
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]

    def get_info(self) -> Dict[str, Any]:
        return {
            "enabled": False,
            "provider": "rule-based",
            "model": None,
        }
