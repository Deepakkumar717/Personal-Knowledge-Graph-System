import re
from typing import List, Optional, Set, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.models.note import Note
from app.repositories.note_repo import NoteRepository
from app.repositories.tag_repo import TagRepository
from app.repositories.link_repo import LinkRepository
from app.repositories.fts_repo import FTSRepository
from app.repositories.trash_repo import TrashRepository
from app.repositories.activity_repo import ActivityRepository
from app.core.exceptions import NotFoundException, ConflictException, ValidationException
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NotePatch,
    NoteDetail,
    NoteListItem,
    NoteBacklinkItem,
    RelatedNoteItem,
    UnlinkedMentionItem,
    NoteDeleteResponse,
)
from app.schemas.link import LinkRead
from app.nlp.normalizer import normalize_title, normalize_content, normalize_tags
from app.nlp.wikilink_parser import (
    extract_wikilinks,
    rewrite_wikilink_in_content,
    FENCED_CODE_BLOCK_PATTERN,
    INLINE_CODE_SPAN_PATTERN,
    WIKILINK_PATTERN,
)
from app.nlp.tfidf import tfidf_engine

class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repo = NoteRepository(db)
        self.tag_repo = TagRepository(db)
        self.link_repo = LinkRepository(db)
        self.fts_repo = FTSRepository(db)
        self.trash_repo = TrashRepository(db)
        self.activity_repo = ActivityRepository(db)

    def _sync_wikilinks_and_pending(self, note: Note) -> None:
        """
        Parse [[...]] from note content, resolve against existing notes,
        and update auto links + pending_links table.
        """
        parsed_titles = extract_wikilinks(note.content, current_note_title=note.title)
        resolved_target_ids: Set[int] = set()
        unresolved_titles_lower: Set[str] = set()

        for target_title in parsed_titles:
            target_note = self.note_repo.get_by_title_lower(target_title)
            if target_note:
                if target_note.id != note.id:
                    resolved_target_ids.add(target_note.id)
            else:
                unresolved_titles_lower.add(target_title.strip().lower())

        self.link_repo.sync_auto_links(
            source_id=note.id,
            resolved_target_ids=resolved_target_ids,
            unresolved_titles_lower=unresolved_titles_lower,
        )

    def _resolve_inbound_pending_links(self, new_note: Note) -> None:
        """
        When note is created or renamed, check if other notes have pending_links
        matching this title. If so, convert them to auto links.
        """
        pending_rows = self.link_repo.find_pending_links_for_title(new_note.title.strip().lower())
        source_ids = {p.source_id for p in pending_rows}
        for src_id in source_ids:
            src_note = self.note_repo.get_by_id(src_id)
            if src_note:
                self._sync_wikilinks_and_pending(src_note)

    def create_note(self, payload: NoteCreate) -> NoteDetail:
        """Create note with title, content, and optional tags & group."""
        title = normalize_title(payload.title)
        content = normalize_content(payload.content)
        tags = normalize_tags(payload.tags)

        # Enforce case-insensitive title uniqueness
        existing = self.note_repo.get_by_title_lower(title)
        if existing:
            raise ConflictException(f"A note with title '{title}' already exists.")

        # Create note
        note = self.note_repo.create(title=title, content=content)
        self.db.flush()

        # Set tags
        self.tag_repo.set_note_tags(note.id, tags)

        # Sync wikilinks & pending links
        self._sync_wikilinks_and_pending(note)

        # Resolve any inbound pending links pointing to this title
        self._resolve_inbound_pending_links(note)

        # Sync FTS
        self.fts_repo.sync_note_fts(note.id, note.title, note.content, tags)

        # Log activity
        self.activity_repo.log(
            action="create",
            entity="note",
            entity_id=note.id,
            title=note.title,
            detail=f"Created note '{note.title}' with {len(tags)} tag(s)",
        )

        self.db.commit()
        tfidf_engine.invalidate()

        return self.get_note_detail(note.id)

    def update_note(self, note_id: int, payload: NoteUpdate) -> NoteDetail:
        """Full update of note title, content, tags, and group."""
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        new_title = normalize_title(payload.title)
        new_content = normalize_content(payload.content)
        new_tags = normalize_tags(payload.tags)
        old_title = note.title

        # Check title uniqueness if title changed (case-insensitive)
        if new_title.lower() != old_title.lower():
            existing = self.note_repo.get_by_title_lower(new_title)
            if existing and existing.id != note_id:
                raise ConflictException(f"A note with title '{new_title}' already exists.")

            # Rewrite wikilinks in other notes referencing old title
            self._propagate_title_rename(old_title, new_title, exclude_note_id=note_id)

        # Update note fields
        self.note_repo.update(note, title=new_title, content=new_content)
        self.tag_repo.set_note_tags(note.id, new_tags)

        # Sync wikilinks & pending links
        self._sync_wikilinks_and_pending(note)

        if new_title.lower() != old_title.lower():
            self._resolve_inbound_pending_links(note)

        # Sync FTS
        self.fts_repo.sync_note_fts(note.id, note.title, note.content, new_tags)

        # Log activity
        self.activity_repo.log(
            action="update",
            entity="note",
            entity_id=note.id,
            title=note.title,
            detail=f"Updated note '{note.title}'",
        )

        self.db.commit()
        tfidf_engine.invalidate()

        return self.get_note_detail(note.id)

    def patch_note(self, note_id: int, payload: NotePatch) -> NoteDetail:
        """Partial update of note title, content, tags, pinned, or group."""
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        old_title = note.title
        new_title = normalize_title(payload.title) if payload.title is not None else note.title
        new_content = normalize_content(payload.content) if payload.content is not None else note.content
        new_pinned = 1 if payload.pinned is True else (0 if payload.pinned is False else note.pinned)
        new_tags = normalize_tags(payload.tags) if payload.tags is not None else [t.name for t in note.tags]

        if payload.title is not None and new_title.lower() != old_title.lower():
            existing = self.note_repo.get_by_title_lower(new_title)
            if existing and existing.id != note_id:
                raise ConflictException(f"A note with title '{new_title}' already exists.")
            self._propagate_title_rename(old_title, new_title, exclude_note_id=note_id)

        self.note_repo.update(note, title=new_title, content=new_content, pinned=new_pinned)
        if payload.tags is not None:
            self.tag_repo.set_note_tags(note.id, new_tags)

        if payload.content is not None or payload.title is not None:
            self._sync_wikilinks_and_pending(note)

        if payload.title is not None and new_title.lower() != old_title.lower():
            self._resolve_inbound_pending_links(note)

        self.fts_repo.sync_note_fts(note.id, note.title, note.content, new_tags)

        self.activity_repo.log(
            action="patch",
            entity="note",
            entity_id=note.id,
            title=note.title,
            detail=f"Patched note '{note.title}'",
        )

        self.db.commit()
        tfidf_engine.invalidate()

        return self.get_note_detail(note.id)

    def _propagate_title_rename(self, old_title: str, new_title: str, exclude_note_id: int) -> None:
        """
        When a note is renamed, find all other notes containing [[Old Title]],
        rewrite to [[New Title]], and re-sync their auto-links & FTS rows.
        """
        referencing_notes = self.note_repo.find_notes_mentioning_title(f"[[{old_title}", exclude_note_id=exclude_note_id)
        for other_note in referencing_notes:
            new_text, modified = rewrite_wikilink_in_content(other_note.content, old_title, new_title)
            if modified:
                other_note.content = new_text
                other_tags = [t.name for t in other_note.tags]
                self._sync_wikilinks_and_pending(other_note)
                self.fts_repo.sync_note_fts(other_note.id, other_note.title, other_note.content, other_tags)

    def delete_note(self, note_id: int) -> NoteDeleteResponse:
        """
        Delete note:
        - Stores full snapshot (title, content, tags, outgoing and incoming links, group) in trash BEFORE deleting.
        - Cascades outgoing and incoming links, note_tags, and FTS row.
        - Leaves [[Deleted]] text in other notes intact, but moves those references to their pending_links.
        """
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        deleted_title = note.title

        # Capture snapshot for Trash before deleting
        outgoing_links_data = [
            {"target_id": l.target_id, "origin": l.origin}
            for l in note.outgoing_links
        ]
        incoming_links_data = [
            {"source_id": l.source_id, "origin": l.origin}
            for l in note.incoming_links
        ]
        snapshot_payload = {
            "title": note.title,
            "content": note.content or "",
            "tags": [t.name for t in note.tags],
            "outgoing_links": outgoing_links_data,
            "incoming_links": incoming_links_data,
            "pinned": bool(note.pinned),
        }
        self.trash_repo.create_snapshot(
            original_note_id=note.id,
            title=note.title,
            payload=snapshot_payload,
        )

        # Find notes that have an outgoing link to this note to record into pending_links
        incoming = self.link_repo.get_incoming_links(note_id)
        source_ids_to_pending = {link.source_id for link, _ in incoming}

        # Delete from FTS
        self.fts_repo.delete_note_fts(note_id)

        # Delete note (DB cascade and relationship cascade handle links, note_tags, and note_groups)
        self.note_repo.delete(note)
        self.db.flush()

        # Record pending links for referencing notes
        for src_id in source_ids_to_pending:
            src_note = self.note_repo.get_by_id(src_id)
            if src_note:
                self._sync_wikilinks_and_pending(src_note)

        # Log activity
        self.activity_repo.log(
            action="delete",
            entity="note",
            entity_id=note_id,
            title=deleted_title,
            detail=f"Deleted note '{deleted_title}' (snapshot saved to trash)",
        )

        self.db.commit()
        tfidf_engine.invalidate()

        return NoteDeleteResponse(
            id=note_id,
            title=deleted_title,
            message="Note deleted successfully.",
        )

    def get_note_detail(self, note_id: int) -> NoteDetail:
        """Fetch complete note details with tags, links, backlinks, unresolved links, related notes, and group."""
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        # Outgoing links
        outgoing_raw = self.link_repo.get_outgoing_links(note_id)
        outgoing_links = [
            LinkRead(
                source_id=l.source_id,
                target_id=l.target_id,
                origin=l.origin,
                source_title=note.title,
                target_title=target.title,
            )
            for l, target in outgoing_raw
        ]

        # Backlinks
        incoming_raw = self.link_repo.get_incoming_links(note_id)
        backlinks = [
            NoteBacklinkItem(
                id=source.id,
                title=source.title,
                origin=l.origin,
            )
            for l, source in incoming_raw
        ]

        # Unresolved links
        unresolved = self.link_repo.get_pending_links(note_id)

        # TF-IDF related notes
        all_notes = self.note_repo.get_all_notes_full()
        doc_data = [
            {"id": n.id, "title": n.title, "content": n.content, "tags": [t.name for t in n.tags]}
            for n in all_notes
        ]
        tfidf_engine.build_index(doc_data)

        # Exclude existing outgoing links and self
        exclude = {l.target_id for l in note.outgoing_links}
        exclude.add(note_id)
        related_raw = tfidf_engine.get_related_notes(note_id, exclude_note_ids=exclude, limit=5)

        note_map = {n.id: n for n in all_notes}
        source_tags = {t.name.lower() for t in note.tags}
        related_notes = []
        for other_id, score in related_raw:
            other_note = note_map.get(other_id)
            if other_note:
                other_tags = {t.name.lower() for t in other_note.tags}
                shared = list(source_tags.intersection(other_tags))
                related_notes.append(
                    RelatedNoteItem(
                        id=other_note.id,
                        title=other_note.title,
                        score=score,
                        shared_tags=shared,
                    )
                )

        return NoteDetail(
            id=note.id,
            title=note.title,
            content=note.content or "",
            tags=[t.name for t in note.tags],
            pinned=bool(note.pinned),
            created_at=note.created_at,
            updated_at=note.updated_at,
            outgoing_links=outgoing_links,
            backlinks=backlinks,
            unresolved_links=unresolved,
            related_notes=related_notes,
        )

    def list_notes(
        self,
        tag: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort: str = "updated",
        pinned: Optional[bool] = None,
    ) -> List[NoteListItem]:
        """List notes with filters and counts."""
        if limit < 1 or limit > 200:
            raise ValidationException("limit must be between 1 and 200.")
        if offset < 0:
            raise ValidationException("offset must be non-negative.")

        rows, _ = self.note_repo.list_notes(
            tag_name=tag,
            query=q,
            limit=limit,
            offset=offset,
            sort_by=sort,
            pinned_only=pinned,
        )
        return [NoteListItem(**r) for r in rows]

    def get_backlinks(self, note_id: int) -> List[NoteBacklinkItem]:
        """Get backlinks only for a note."""
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        incoming = self.link_repo.get_incoming_links(note_id)
        return [
            NoteBacklinkItem(
                id=source.id,
                title=source.title,
                origin=l.origin,
            )
            for l, source in incoming
        ]

    def get_related_notes(self, note_id: int, limit: int = 5) -> List[RelatedNoteItem]:
        """Get TF-IDF related notes."""
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        all_notes = self.note_repo.get_all_notes_full()
        doc_data = [
            {"id": n.id, "title": n.title, "content": n.content, "tags": [t.name for t in n.tags]}
            for n in all_notes
        ]
        tfidf_engine.build_index(doc_data)

        exclude = {l.target_id for l in note.outgoing_links}
        exclude.add(note_id)
        related_raw = tfidf_engine.get_related_notes(note_id, exclude_note_ids=exclude, limit=limit)

        note_map = {n.id: n for n in all_notes}
        source_tags = {t.name.lower() for t in note.tags}
        results = []
        for other_id, score in related_raw:
            other = note_map.get(other_id)
            if other:
                other_tags = {t.name.lower() for t in other.tags}
                shared = list(source_tags.intersection(other_tags))
                results.append(
                    RelatedNoteItem(
                        id=other.id,
                        title=other.title,
                        score=score,
                        shared_tags=shared,
                    )
                )
        return results

    def get_unlinked_mentions(self, note_id: int) -> List[UnlinkedMentionItem]:
        """Find unlinked mentions."""
        target_note = self.note_repo.get_by_id(note_id)
        if not target_note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        target_title = target_note.title.strip()
        if not target_title:
            return []

        mention_regex = re.compile(rf"\b{re.escape(target_title)}\b", re.IGNORECASE)

        all_notes = self.note_repo.get_all_notes_full()
        mentions = []

        for other_note in all_notes:
            if other_note.id == note_id:
                continue

            content = other_note.content or ""
            cleaned = FENCED_CODE_BLOCK_PATTERN.sub(" ", content)
            cleaned = INLINE_CODE_SPAN_PATTERN.sub(" ", cleaned)
            cleaned = WIKILINK_PATTERN.sub(" ", cleaned)

            match = mention_regex.search(cleaned)
            if match:
                start = max(0, match.start() - 40)
                end = min(len(cleaned), match.end() + 40)
                snippet = cleaned[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(cleaned):
                    snippet = snippet + "..."

                mentions.append(
                    UnlinkedMentionItem(
                        note_id=other_note.id,
                        note_title=other_note.title,
                        snippet=snippet,
                    )
                )

        return mentions
