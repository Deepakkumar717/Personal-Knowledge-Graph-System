from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from app.repositories.tag_repo import TagRepository
from app.repositories.note_repo import NoteRepository
from app.schemas.tag import TagUsage, TagSuggestion, TagSuggestResponse
from app.nlp.tag_suggester import suggest_tags
from app.nlp.normalizer import normalize_tags

class TagService:
    def __init__(self, db: Session):
        self.db = db
        self.tag_repo = TagRepository(db)
        self.note_repo = NoteRepository(db)

    def list_all_tags(self) -> List[TagUsage]:
        """Get all tags with usage counts."""
        tags_with_counts = self.tag_repo.get_all_tags_with_counts()
        return [
            TagUsage(id=t.id, name=t.name, count=count)
            for t, count in tags_with_counts
        ]

    def suggest_tags(
        self,
        query: str = "",
        selected_tags: Optional[List[str]] = None,
        note_content: Optional[str] = None,
        limit: int = 10,
    ) -> TagSuggestResponse:
        """Suggest relevant tags based on query, selected tags, and note content."""
        tags_with_counts = self.tag_repo.get_all_tags_with_counts()
        counts_list = [(t.name, count) for t, count in tags_with_counts]
        co_matrix = self.tag_repo.get_tag_co_occurrences()

        suggestions_raw = suggest_tags(
            query=query,
            selected_tags=selected_tags or [],
            all_tags_with_counts=counts_list,
            tag_co_occurrences=co_matrix,
            note_content=note_content,
            limit=limit,
        )

        suggestions = [
            TagSuggestion(name=s["name"], count=s["count"], score=s["score"])
            for s in suggestions_raw
        ]

        return TagSuggestResponse(query=query, suggestions=suggestions)

    def cleanup_orphaned_tags(self) -> int:
        """Delete tags not used in any notes."""
        return self.tag_repo.delete_orphaned_tags()
