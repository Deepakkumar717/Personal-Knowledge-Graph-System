import re
from typing import List, Optional, Set
from sqlalchemy.orm import Session
from app.repositories.link_repo import LinkRepository
from app.repositories.note_repo import NoteRepository
from app.repositories.fts_repo import FTSRepository
from app.core.exceptions import NotFoundException, BadRequestException, ConflictException
from app.schemas.link import LinkRead, LinkDeleteResponse, SuggestedLinkRead
from app.nlp.tfidf import tfidf_engine

class LinkService:
    def __init__(self, db: Session):
        self.db = db
        self.link_repo = LinkRepository(db)
        self.note_repo = NoteRepository(db)
        self.fts_repo = FTSRepository(db)

    def create_manual_link(self, source_id: int, target_id: int) -> LinkRead:
        """Create a manual directed link from source to target."""
        if source_id == target_id:
            raise BadRequestException("Cannot link a note to itself (self-loop not allowed).")

        source_note = self.note_repo.get_by_id(source_id)
        if not source_note:
            raise NotFoundException(f"Source note with id {source_id} not found.")

        target_note = self.note_repo.get_by_id(target_id)
        if not target_note:
            raise NotFoundException(f"Target note with id {target_id} not found.")

        existing = self.link_repo.get_link(source_id, target_id)
        if existing:
            raise ConflictException(f"Link already exists between Note {source_id} and Note {target_id}.")

        link = self.link_repo.add_link(source_id, target_id, origin="manual")
        self.db.commit()

        return LinkRead(
            source_id=link.source_id,
            target_id=link.target_id,
            origin=link.origin,
            source_title=source_note.title,
            target_title=target_note.title,
        )

    def delete_link(self, source_id: int, target_id: int) -> LinkDeleteResponse:
        """
        Delete a directed link between source and target.
        If the link was origin='auto', we also remove the [[Target Title]] text from source note content
        so it is not resurrected automatically on future edits.
        """
        source_note = self.note_repo.get_by_id(source_id)
        if not source_note:
            raise NotFoundException(f"Source note with id {source_id} not found.")

        target_note = self.note_repo.get_by_id(target_id)
        if not target_note:
            raise NotFoundException(f"Target note with id {target_id} not found.")

        link = self.link_repo.get_link(source_id, target_id)
        if not link:
            raise NotFoundException(f"Link from note {source_id} to note {target_id} not found.")

        # If it was an auto link, strip the [[Target]] wikilink from source content to prevent re-creation
        if link.origin == "auto" and source_note.content:
            target_title = target_note.title
            # Regex to remove [[Target]] or [[Target|Alias]]
            pattern = re.compile(rf"\[\[{re.escape(target_title)}(\|[^\]]*)?\]\]", re.IGNORECASE)
            source_note.content = pattern.sub(target_title, source_note.content)
            tag_names = [t.name for t in source_note.tags]
            self.fts_repo.sync_note_fts(source_note.id, source_note.title, source_note.content, tag_names)

        self.link_repo.delete_link(source_id, target_id)
        self.db.commit()

        return LinkDeleteResponse(
            source_id=source_id,
            target_id=target_id,
            message="Link successfully removed.",
        )

    def get_suggested_links(self, note_id: int, limit: int = 5) -> List[SuggestedLinkRead]:
        """Suggest links for a note using TF-IDF similarity + shared tags, excluding existing links."""
        source_note = self.note_repo.get_by_id(note_id)
        if not source_note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        # Rebuild TF-IDF if needed
        all_notes = self.note_repo.get_all_notes_full()
        doc_data = [
            {"id": n.id, "title": n.title, "content": n.content, "tags": [t.name for t in n.tags]}
            for n in all_notes
        ]
        tfidf_engine.build_index(doc_data)

        # Exclude existing outgoing and incoming linked notes
        existing_targets = {l.target_id for l in source_note.outgoing_links}
        existing_sources = {l.source_id for l in source_note.incoming_links}
        exclude = existing_targets.union(existing_sources)
        exclude.add(note_id)

        source_tags = {t.name.lower() for t in source_note.tags}
        related = tfidf_engine.get_related_notes(note_id, exclude_note_ids=exclude, limit=limit)

        notes_map = {n.id: n for n in all_notes}
        results = []
        for other_id, score in related:
            target_note = notes_map.get(other_id)
            if target_note:
                other_tags = {t.name.lower() for t in target_note.tags}
                shared = list(source_tags.intersection(other_tags))
                results.append(
                    SuggestedLinkRead(
                        target_id=target_note.id,
                        target_title=target_note.title,
                        similarity_score=score,
                        shared_tags=shared,
                    )
                )

        return results
