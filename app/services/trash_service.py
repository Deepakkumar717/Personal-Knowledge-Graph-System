import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.trash_repo import TrashRepository
from app.repositories.note_repo import NoteRepository
from app.repositories.tag_repo import TagRepository
from app.repositories.link_repo import LinkRepository
from app.repositories.fts_repo import FTSRepository
from app.repositories.activity_repo import ActivityRepository
from app.nlp.normalizer import normalize_tags
from app.nlp.tfidf import tfidf_engine
from app.schemas.safety import TrashItem, TrashDetail
from app.schemas.note import NoteDetail
from app.core.exceptions import NotFoundException, ConflictException

class TrashService:
    def __init__(self, db: Session):
        self.db = db
        self.trash_repo = TrashRepository(db)
        self.note_repo = NoteRepository(db)
        self.tag_repo = TagRepository(db)
        self.link_repo = LinkRepository(db)
        self.fts_repo = FTSRepository(db)
        self.activity_repo = ActivityRepository(db)

    def list_trash(self) -> List[TrashItem]:
        # Clean up records older than 30 days first (purges only trash rows, never live notes)
        self.trash_repo.purge_older_than(days=30)
        self.db.commit()

        records = self.trash_repo.list_all()
        return [
            TrashItem(
                id=r.id,
                original_note_id=r.original_note_id,
                title=r.title,
                deleted_at=r.deleted_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            for r in records
        ]

    def get_trash_detail(self, trash_id: int) -> TrashDetail:
        record = self.trash_repo.get_by_id(trash_id)
        if not record:
            raise NotFoundException(f"Trash item {trash_id} not found.")
        payload = json.loads(record.payload_json)
        return TrashDetail(
            id=record.id,
            original_note_id=record.original_note_id,
            title=record.title,
            deleted_at=record.deleted_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            payload=payload,
        )

    def restore_note(self, trash_id: int) -> NoteDetail:
        record = self.trash_repo.get_by_id(trash_id)
        if not record:
            raise NotFoundException(f"Trash item {trash_id} not found.")

        payload = json.loads(record.payload_json)
        title = payload.get("title", record.title)
        content = payload.get("content", "")
        raw_tags = payload.get("tags", [])
        pinned = payload.get("pinned", False)
        outgoing_links_data = payload.get("outgoing_links", [])
        incoming_links_data = payload.get("incoming_links", [])

        # Check if title already taken
        existing = self.note_repo.get_by_title_lower(title)
        if existing:
            raise ConflictException(f"Cannot restore: A note with title '{title}' already exists.")

        # Recreate note
        new_note = self.note_repo.create(title=title, content=content, pinned=1 if pinned else 0)

        # Restore tags
        norm_tags = normalize_tags(raw_tags)
        self.tag_repo.set_note_tags(new_note.id, norm_tags)

        # Sync FTS
        self.fts_repo.sync_note_fts(new_note.id, title, content, norm_tags)

        # Restore links where other end still exists
        for link_info in outgoing_links_data:
            target_id = link_info.get("target_id")
            origin = link_info.get("origin", "manual")
            if target_id and self.note_repo.get_by_id(target_id):
                if not self.link_repo.get_link(new_note.id, target_id):
                    self.link_repo.add_link(new_note.id, target_id, origin=origin)

        for link_info in incoming_links_data:
            source_id = link_info.get("source_id")
            origin = link_info.get("origin", "manual")
            if source_id and self.note_repo.get_by_id(source_id):
                if not self.link_repo.get_link(source_id, new_note.id):
                    self.link_repo.add_link(source_id, new_note.id, origin=origin)

        # Delete from trash
        self.trash_repo.delete(trash_id)

        # Log activity
        self.activity_repo.log(
            action="restore",
            entity="note",
            entity_id=new_note.id,
            title=new_note.title,
            detail=f"Restored note '{new_note.title}' from trash",
        )

        self.db.commit()
        tfidf_engine.invalidate()

        from app.services.note_service import NoteService
        return NoteService(self.db).get_note_detail(new_note.id)

    def delete_trash_item(self, trash_id: int) -> bool:
        record = self.trash_repo.get_by_id(trash_id)
        if not record:
            raise NotFoundException(f"Trash item {trash_id} not found.")
        title = record.title
        self.trash_repo.delete(trash_id)
        self.activity_repo.log(
            action="permanent_delete",
            entity="trash",
            entity_id=trash_id,
            title=title,
            detail=f"Permanently deleted '{title}' from trash",
        )
        self.db.commit()
        return True

    def empty_trash(self) -> int:
        count = self.trash_repo.empty_trash()
        self.activity_repo.log(
            action="empty",
            entity="trash",
            detail=f"Emptied trash ({count} items permanently deleted)",
        )
        self.db.commit()
        return count
