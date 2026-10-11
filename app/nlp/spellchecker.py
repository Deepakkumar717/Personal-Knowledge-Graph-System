import os
import re
from typing import Set, List, Optional
import difflib

class OfflineSpellChecker:
    """
    Fast, deterministic, offline spellchecker using a bundled dictionary
    and edit-distance / difflib ranking.
    """
    def __init__(self, dict_path: Optional[str] = None):
        if dict_path is None:
            dict_path = os.path.join(os.path.dirname(__file__), "dictionary.txt")
        self.words: Set[str] = set()
        self.word_list: List[str] = []
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                for line in f:
                    w = line.strip().lower()
                    if w and not w.startswith("#"):
                        self.words.add(w)
                        self.word_list.append(w)

    def is_known(self, word: str) -> bool:
        return word.lower() in self.words

    def add_known_words(self, words: List[str]):
        for w in words:
            clean = w.strip().lower()
            if clean:
                self.words.add(clean)
                if clean not in self.word_list:
                    self.word_list.append(clean)

    def _edits1(self, word: str) -> Set[str]:
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word: str) -> Set[str]:
        return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))

    def suggest(self, word: str, custom_pool: Optional[List[str]] = None, max_results: int = 3) -> List[str]:
        clean = word.lower().strip()
        if not clean or len(clean) < 2:
            return []

        # If already known, no correction needed
        pool_set = set(custom_pool) if custom_pool else set()
        if clean in self.words or clean in pool_set:
            return []

        # 1. Check custom pool fuzzy match first (e.g. existing tags or note titles)
        if custom_pool:
            close_custom = difflib.get_close_matches(clean, custom_pool, n=max_results, cutoff=0.72)
            if close_custom:
                return close_custom

        # 2. Distance 1 edits in dictionary
        e1 = self._edits1(clean)
        known_e1 = [w for w in self.word_list if w in e1]
        if known_e1:
            return known_e1[:max_results]

        # 3. Distance 2 edits in dictionary for shorter words
        if len(clean) <= 8:
            e2 = self._edits2(clean)
            known_e2 = [w for w in self.word_list if w in e2]
            if known_e2:
                return known_e2[:max_results]

        # 4. Difflib close matches fallback
        matches = difflib.get_close_matches(clean, self.word_list, n=max_results, cutoff=0.70)
        return matches

# Global singleton
spellchecker = OfflineSpellChecker()
