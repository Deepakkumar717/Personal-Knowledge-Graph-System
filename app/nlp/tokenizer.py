import re
from typing import List, Set
from app.nlp.stopwords import ENGLISH_STOP_WORDS
from app.nlp.stemmer import stem_word

WORD_PATTERN = re.compile(r"[a-zA-Z0-9_\-]+")

def tokenize(
    text: str,
    remove_stopwords: bool = True,
    stem: bool = False,
    min_length: int = 2,
) -> List[str]:
    """Tokenize a given string into words with optional stopword removal and stemming."""
    if not text:
        return []

    words = WORD_PATTERN.findall(text.lower())
    tokens = []
    for word in words:
        # Strip leading/trailing hyphens or underscores
        w = word.strip("-_")
        if len(w) < min_length:
            continue
        if remove_stopwords and w in ENGLISH_STOP_WORDS:
            continue
        if stem:
            w = stem_word(w)
        tokens.append(w)
    return tokens
