from abc import ABC, abstractmethod
from typing import List, Dict, Any, Set, Tuple, Optional

class AssistProvider(ABC):
    """
    Abstract interface for AI/Rule-based suggestions.
    All outputs from providers are strictly suggestions and never mutate notes/links directly.
    """

    @abstractmethod
    def suggest_tags(
        self,
        title: str,
        content: str,
        current_tags: List[str],
        existing_tags: List[str],
        corpus_bigrams: Set[Tuple[str, str]],
    ) -> Dict[str, Any]:
        """Returns {normalized, suggestions, merges, corrections}"""
        pass

    @abstractmethod
    def proofread(
        self,
        text: str,
        known_titles: List[str],
        known_tags: List[str],
        ignored_words: List[str],
    ) -> List[Dict[str, Any]]:
        """Returns list of {start, end, original, suggestion, reason}"""
        pass

    @abstractmethod
    def suggest_links(
        self,
        note_id: int,
        note_title: str,
        note_content: str,
        note_tags: List[str],
        candidates: List[Dict[str, Any]],
        dismissed_ids: Set[int],
    ) -> List[Dict[str, Any]]:
        """Returns list of {note_id, title, score, reasons}"""
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Returns metadata about the active provider"""
        pass
