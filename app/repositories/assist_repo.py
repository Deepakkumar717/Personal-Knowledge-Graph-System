import re
from typing import Set, Tuple, List, Optional
from collections import Counter
from sqlalchemy.orm import Session
from app.models.dismissed_suggestion import DismissedSuggestion
from app.models.note import Note

class AssistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_dismissed_ids(self, note_id: int) -> Set[int]:
        """Returns set of note IDs dismissed for suggestions with this note."""
        results = (
            self.db.query(DismissedSuggestion.other_id)
            .filter(DismissedSuggestion.note_id == note_id)
            .all()
        )
        return {r[0] for r in results}

    def dismiss_suggestion(self, note_id: int, other_id: int) -> None:
        """Adds a dismissed suggestion pair if not already present."""
        existing = (
            self.db.query(DismissedSuggestion)
            .filter(
                DismissedSuggestion.note_id == note_id,
                DismissedSuggestion.other_id == other_id,
            )
            .first()
        )
        if not existing:
            entry = DismissedSuggestion(note_id=note_id, other_id=other_id)
            self.db.add(entry)
            self.db.commit()

    def get_corpus_bigrams(self, min_freq: int = 2) -> Set[Tuple[str, str]]:
        """
        Extracts frequent two-word token pairs from all notes in the database.
        """
        notes = self.db.query(Note.title, Note.content).all()
        bigram_counts: Counter = Counter()

        for title, content in notes:
            text = f"{title or ''} {content or ''}".lower()
            tokens = re.findall(r"\b[a-z]{2,}\b", text)
            for i in range(len(tokens) - 1):
                bigram_counts[(tokens[i], tokens[i + 1])] += 1

        frequent = {bg for bg, count in bigram_counts.items() if count >= min_freq}
        return frequent
