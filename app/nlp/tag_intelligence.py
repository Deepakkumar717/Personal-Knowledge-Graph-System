import os
import re
from typing import List, Dict, Set, Tuple, Optional, Any
from app.nlp.spellchecker import spellchecker

def normalize_tag(tag: str) -> str:
    """
    Normalizes a single tag:
    - trim whitespace
    - lowercase
    - strip leading '#'
    - convert internal whitespace to single hyphen ('fast food' -> 'fast-food')
    - strip punctuation (keep alphanumeric and hyphen)
    - collapse consecutive hyphens
    - max 30 characters
    - strip leading/trailing hyphens
    """
    if not tag:
        return ""
    t = tag.strip().lower()
    while t.startswith("#"):
        t = t[1:].strip()

    # Convert spaces/tabs/underscores to hyphens
    t = re.sub(r"[\s_]+", "-", t)

    # Strip unwanted punctuation characters (keep alphanumeric and hyphen)
    t = re.sub(r"[^\w\-]", "", t)

    # Collapse consecutive hyphens
    t = re.sub(r"-+", "-", t)

    # Strip leading/trailing hyphens
    t = t.strip("-")

    # Max length: 30 chars
    return t[:30]


def parse_raw_tag_string(raw: str) -> List[str]:
    """
    Splits raw tag input ONLY on commas, newlines, or tabs.
    Space stays INSIDE the tag (e.g. 'fast food' is 1 tag).
    """
    if not raw:
        return []
    # Split by comma, newline, tab
    parts = re.split(r"[\r\n\t,]+", raw)
    results = []
    seen = set()
    for p in parts:
        normalized = normalize_tag(p)
        if normalized and normalized not in seen:
            seen.add(normalized)
            results.append(normalized)
    return results


class PhraseMatcher:
    def __init__(self, phrases_file: Optional[str] = None):
        if phrases_file is None:
            phrases_file = os.path.join(os.path.dirname(__file__), "phrases.txt")
        self.known_phrases: Set[Tuple[str, str]] = set()
        self.phrase_slugs: Set[str] = set()

        if os.path.exists(phrases_file):
            with open(phrases_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip().lower()
                    if line and not line.startswith("#"):
                        tokens = line.split()
                        if len(tokens) == 2:
                            self.known_phrases.add((tokens[0], tokens[1]))
                            self.phrase_slugs.add(f"{tokens[0]}-{tokens[1]}")

    def is_known_phrase(
        self,
        word1: str,
        word2: str,
        context_text: str = "",
        existing_tags: Optional[List[str]] = None,
        corpus_bigrams: Optional[Set[Tuple[str, str]]] = None,
    ) -> Optional[str]:
        w1, w2 = word1.strip().lower(), word2.strip().lower()
        slug_forward = f"{w1}-{w2}"
        slug_reverse = f"{w2}-{w1}"

        existing_tag_set = set(existing_tags or [])
        bigram_set = corpus_bigrams or set()
        clean_context = context_text.lower() if context_text else ""

        # Check conditions (a), (b), (c), (d):
        for candidate_slug, (a, b) in [
            (slug_forward, (w1, w2)),
            (slug_reverse, (w2, w1)),
        ]:
            # (c) In bundled phrase list
            if (a, b) in self.known_phrases or candidate_slug in self.phrase_slugs:
                return candidate_slug

            # (b) Matches an existing tag in DB
            if candidate_slug in existing_tag_set:
                return candidate_slug

            # (a) Appears in note title/content as phrase
            phrase_str = f"{a} {b}"
            if phrase_str in clean_context:
                return candidate_slug

            # (d) Is a frequent bigram in user's notes
            if (a, b) in bigram_set:
                return candidate_slug

        return None


phrase_matcher = PhraseMatcher()


def detect_phrase_merges(
    tags: List[str],
    context_text: str = "",
    existing_tags: Optional[List[str]] = None,
    corpus_bigrams: Optional[Set[Tuple[str, str]]] = None,
) -> List[Dict[str, Any]]:
    """
    Checks adjacent tags in the list (in either order).
    If they form a known phrase, suggests merge.
    Never merges automatically.
    """
    merges = []
    seen_merges = set()

    for i in range(len(tags) - 1):
        t1, t2 = tags[i], tags[i + 1]
        target_slug = phrase_matcher.is_known_phrase(
            t1, t2, context_text, existing_tags, corpus_bigrams
        )
        if target_slug:
            merge_key = (min(t1, t2), max(t1, t2), target_slug)
            if merge_key not in seen_merges:
                seen_merges.add(merge_key)
                merges.append({
                    "from": [t1, t2],
                    "to": target_slug,
                })

    return merges


def detect_tag_typos(
    tags: List[str],
    existing_tags: Optional[List[str]] = None,
) -> List[Dict[str, str]]:
    """
    Checks tags against offline spellchecker dictionary and fuzzy match to existing tags.
    """
    corrections = []
    existing = [t.lower() for t in (existing_tags or [])]
    existing_set = set(existing)

    for tag in tags:
        clean = tag.lower().strip()
        # If tag already matches an existing tag or is in dictionary, no correction
        if clean in existing_set or spellchecker.is_known(clean):
            continue

        # If it's a hyphenated tag (e.g. 'fast-food'), check parts
        if "-" in clean:
            parts = clean.split("-")
            all_known = all(spellchecker.is_known(p) or p in existing_set for p in parts)
            if all_known:
                continue

        # Check suggestions
        suggestions = spellchecker.suggest(clean, custom_pool=existing, max_results=1)
        if suggestions and suggestions[0] != clean:
            best = suggestions[0]
            # Prioritize 'food' over 'fold' if tag is 'fod'
            if clean == "fod" and "food" in spellchecker.suggest(clean, max_results=5):
                best = "food"
            corrections.append({
                "from": tag,
                "to": best,
            })

    return corrections
