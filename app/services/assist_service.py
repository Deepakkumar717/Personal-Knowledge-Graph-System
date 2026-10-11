import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.note_repo import NoteRepository
from app.repositories.tag_repo import TagRepository
from app.repositories.link_repo import LinkRepository
from app.repositories.assist_repo import AssistRepository
from app.assist.provider import AssistProvider
from app.assist.rule_provider import RuleBasedProvider
from app.assist.llm_provider import LLMProvider

class AssistService:
    def __init__(self, db: Session, provider: Optional[AssistProvider] = None):
        self.db = db
        self.note_repo = NoteRepository(db)
        self.tag_repo = TagRepository(db)
        self.link_repo = LinkRepository(db)
        self.assist_repo = AssistRepository(db)

        if provider is not None:
            self.provider = provider
        else:
            # Check environment to select provider
            ai_enabled = os.getenv("AI_ENABLED", "false").lower() in ("true", "1", "yes")
            if ai_enabled:
                self.provider = LLMProvider()
            else:
                self.provider = RuleBasedProvider()

    def get_status(self) -> Dict[str, Any]:
        return self.provider.get_info()

    def assist_tags(
        self,
        title: Optional[str],
        content: Optional[str],
        tags: List[str],
    ) -> Dict[str, Any]:
        existing_tags_tuples = self.tag_repo.get_all_tags_with_counts()
        existing_tags = [t.name for t, _ in existing_tags_tuples]
        corpus_bigrams = self.assist_repo.get_corpus_bigrams()

        return self.provider.suggest_tags(
            title=title or "",
            content=content or "",
            current_tags=tags or [],
            existing_tags=existing_tags,
            corpus_bigrams=corpus_bigrams,
        )

    def proofread(
        self,
        text: str,
        ignored_words: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        # Fetch known titles and tags to exempt them
        all_notes = self.note_repo.get_all_notes_full()
        known_titles = [n.title for n in all_notes]

        existing_tags_tuples = self.tag_repo.get_all_tags_with_counts()
        known_tags = [t.name for t, _ in existing_tags_tuples]

        return self.provider.proofread(
            text=text,
            known_titles=known_titles,
            known_tags=known_tags,
            ignored_words=ignored_words or [],
        )

    def get_link_suggestions(self, note_id: int) -> List[Dict[str, Any]]:
        note = self.note_repo.get_by_id(note_id)
        if not note:
            return []

        dismissed_ids = self.assist_repo.get_dismissed_ids(note_id)

        # Get existing outgoing and incoming links for note
        outgoing_links = self.link_repo.get_outgoing_links(note_id)
        outgoing_target_ids = {link.target_id for link, _ in outgoing_links}
        backlinks = self.link_repo.get_incoming_links(note_id)
        backlink_source_ids = {link.source_id for link, _ in backlinks}
        already_linked_ids = outgoing_target_ids.union(backlink_source_ids)

        # Gather mutual neighbours for each potential candidate
        all_notes = self.note_repo.get_all_notes_full()
        candidates: List[Dict[str, Any]] = []

        # Find 1-hop neighbours of target note
        note_neighbours = outgoing_target_ids.union(backlink_source_ids)

        for other in all_notes:
            if other.id == note_id:
                continue

            # Candidate 1-hop neighbours
            other_outgoing = {l.target_id for l, _ in self.link_repo.get_outgoing_links(other.id)}
            other_backlinks = {l.source_id for l, _ in self.link_repo.get_incoming_links(other.id)}
            other_neighbours = other_outgoing.union(other_backlinks)

            shared_neighbour_ids = note_neighbours.intersection(other_neighbours)
            shared_neighbour_titles = [
                n.title for n in all_notes if n.id in shared_neighbour_ids
            ]

            candidates.append({
                "id": other.id,
                "title": other.title,
                "content": other.content or "",
                "tags": [t.name for t in other.tags],
                "already_linked": other.id in outgoing_target_ids,
                "shared_neighbours": shared_neighbour_titles,
            })

        note_tags = [t.name for t in note.tags]
        return self.provider.suggest_links(
            note_id=note_id,
            note_title=note.title,
            note_content=note.content or "",
            note_tags=note_tags,
            candidates=candidates,
            dismissed_ids=dismissed_ids,
        )

    def dismiss_link_suggestion(self, note_id: int, other_id: int) -> Dict[str, Any]:
        self.assist_repo.dismiss_suggestion(note_id, other_id)
        return {
            "status": "success",
            "message": f"Dismissed link suggestion between note {note_id} and note {other_id}.",
        }
