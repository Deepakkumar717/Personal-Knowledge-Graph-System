from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from app.nlp.fuzzy import fuzzy_score
from app.nlp.normalizer import normalize_single_tag
from app.nlp.tfidf import tfidf_engine

def suggest_tags(
    query: str,
    selected_tags: List[str],
    all_tags_with_counts: List[Tuple[str, int]],  # (tag_name, usage_count)
    tag_co_occurrences: Dict[str, Dict[str, int]],  # tag -> other_tag -> count
    note_content: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, any]]:
    """
    Suggest tags based on:
    1. Prefix matching
    2. Fuzzy matching on query
    3. Usage count ranking
    4. Co-occurrence boost with already selected tags
    5. TF-IDF keywords extracted from note content matching existing tags
    """
    selected_set = {normalize_single_tag(t) for t in selected_tags if normalize_single_tag(t)}
    q_norm = normalize_single_tag(query) or ""

    # Top keywords from note content
    content_keywords = set()
    if note_content:
        raw_kws = tfidf_engine.extract_top_keywords(note_content, top_k=15)
        for kw in raw_kws:
            norm_kw = normalize_single_tag(kw)
            if norm_kw:
                content_keywords.add(norm_kw)

    scored_tags = []

    for tag_name, count in all_tags_with_counts:
        norm_name = normalize_single_tag(tag_name)
        if not norm_name or norm_name in selected_set:
            continue

        base_score = 0.0

        # Query matching
        if q_norm:
            if norm_name.startswith(q_norm):
                # Prefix match bonus
                base_score += 10.0 + (5.0 * len(q_norm) / len(norm_name))
            elif q_norm in norm_name:
                # Substring match
                base_score += 6.0
            else:
                # Fuzzy match
                f_score = fuzzy_score(q_norm, norm_name)
                if f_score > 0.6:
                    base_score += f_score * 5.0
                else:
                    # Query provided and tag didn't match closely -> skip
                    continue
        else:
            # When no query, base score comes from popularity
            base_score += 1.0

        # Popularity weighting (log scale)
        base_score += min(5.0, count * 0.5)

        # Co-occurrence boost with selected tags
        co_score = 0.0
        if selected_set and norm_name in tag_co_occurrences:
            for s_tag in selected_set:
                co_count = tag_co_occurrences[norm_name].get(s_tag, 0)
                co_score += min(5.0, co_count * 1.5)
        base_score += co_score

        # Content keyword match boost
        if norm_name in content_keywords:
            base_score += 4.0

        scored_tags.append({
            "name": norm_name,
            "count": count,
            "score": round(base_score, 2),
        })

    scored_tags.sort(key=lambda x: x["score"], reverse=True)
    return scored_tags[:limit]
