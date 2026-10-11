import re

# Standard English suffix rules for light stemming
SUFFIXES = [
    ("sses", "ss"),
    ("ies", "i"),
    ("eed", "ee"),
    ("ing", ""),
    ("ed", ""),
    ("ational", "ate"),
    ("tional", "tion"),
    ("enci", "ence"),
    ("anci", "ance"),
    ("izer", "ize"),
    ("bli", "ble"),
    ("alli", "al"),
    ("entli", "ent"),
    ("eli", "e"),
    ("ousli", "ous"),
    ("ization", "ize"),
    ("ation", "ate"),
    ("ator", "ate"),
    ("alism", "al"),
    ("iveness", "ive"),
    ("fulness", "ful"),
    ("ousness", "ous"),
    ("aliti", "al"),
    ("iviti", "ive"),
    ("biliti", "ble"),
    ("icate", "ic"),
    ("ative", ""),
    ("alize", "al"),
    ("iciti", "ic"),
    ("ical", "ic"),
    ("ful", ""),
    ("ness", ""),
    ("able", ""),
    ("ible", ""),
    ("ment", ""),
    ("ant", ""),
    ("ent", ""),
    ("ism", ""),
    ("ist", ""),
    ("ive", ""),
    ("ize", ""),
    ("ly", ""),
    ("s", ""),
]

def stem_word(word: str) -> str:
    """Lightweight pure-Python suffix stemmer."""
    word = word.lower()
    if len(word) <= 3:
        return word

    for suffix, replacement in SUFFIXES:
        if word.endswith(suffix):
            stem = word[:-len(suffix)] + replacement
            if len(stem) >= 3:
                return stem
    return word
