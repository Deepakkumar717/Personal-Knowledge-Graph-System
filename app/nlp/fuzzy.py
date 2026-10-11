import difflib
from typing import List, Tuple, Dict, Any

def fuzzy_score(query: str, target: str) -> float:
    """
    Compute normalized fuzzy similarity ratio between 0.0 and 1.0.
    Checks full string match, substring match, and word-level matches.
    """
    q = query.strip().lower()
    t = target.strip().lower()
    if not q or not t:
        return 0.0
    if q == t:
        return 1.0
    if q in t:
        return 0.85 + (0.15 * len(q) / len(t))

    # Full ratio
    full_ratio = difflib.SequenceMatcher(None, q, t).ratio()

    # Word-level best ratio
    words = [w.strip() for w in t.split() if w.strip()]
    best_word_ratio = 0.0
    for w in words:
        if q == w:
            best_word_ratio = max(best_word_ratio, 0.95)
        elif q in w:
            best_word_ratio = max(best_word_ratio, 0.85)
        else:
            w_ratio = difflib.SequenceMatcher(None, q, w).ratio()
            best_word_ratio = max(best_word_ratio, w_ratio)

    return max(full_ratio, best_word_ratio)

def find_fuzzy_matches(
    query: str,
    candidates: List[Tuple[Any, str]],  # (item, text_to_match)
    threshold: float = 0.55,
    limit: int = 10,
) -> List[Tuple[Any, float]]:
    """
    Search candidate strings using fuzzy similarity.
    Returns list of (item, score) sorted descending by score.
    """
    if not query:
        return []

    q_lower = query.strip().lower()
    scored = []
    for item, text in candidates:
        score = fuzzy_score(q_lower, text)
        if score >= threshold:
            scored.append((item, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]
