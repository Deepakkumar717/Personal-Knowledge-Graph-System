from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy import text, func, desc, asc
from sqlalchemy.orm import Session
from app.models.note import Note
from app.models.tag import Tag
from app.models.note_tag import NoteTag
from app.models.link import Link

class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, note_id: int) -> Optional[Note]:
        """Fetch note by ID."""
        return self.db.query(Note).filter(Note.id == note_id).first()

    def get_by_title_lower(self, title_lower: str) -> Optional[Note]:
        """Fetch note by case-insensitive lower title."""
        return self.db.query(Note).filter(func.lower(Note.title) == title_lower.strip().lower()).first()

    def create(self, title: str, content: str = "", pinned: int = 0) -> Note:
        """Insert a new note record."""
        now = datetime.now(timezone.utc)
        note = Note(
            title=title.strip(),
            content=content or "",
            pinned=pinned,
            created_at=now,
            updated_at=now,
        )
        self.db.add(note)
        self.db.flush()
        return note

    def update(self, note: Note, title: Optional[str] = None, content: Optional[str] = None, pinned: Optional[int] = None) -> Note:
        """Update fields of an existing note."""
        if title is not None:
            note.title = title.strip()
        if content is not None:
            note.content = content
        if pinned is not None:
            note.pinned = pinned
        note.updated_at = datetime.now(timezone.utc)
        self.db.flush()
        return note

    def delete(self, note: Note) -> None:
        """Delete note record."""
        self.db.delete(note)
        self.db.flush()

    def list_notes(
        self,
        tag_name: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "updated",
        pinned_only: Optional[bool] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        List notes with pagination, sorting, tag filter, query filter, and counts.
        Returns (list_of_note_dict, total_count).
        """
        base_query = self.db.query(Note)

        if pinned_only is not None:
            base_query = base_query.filter(Note.pinned == (1 if pinned_only else 0))

        if tag_name:
            base_query = (
                base_query.join(NoteTag, NoteTag.note_id == Note.id)
                .join(Tag, Tag.id == NoteTag.tag_id)
                .filter(func.lower(Tag.name) == tag_name.lower())
            )

        if query:
            q_clean = f"%{query.strip().lower()}%"
            base_query = base_query.filter(
                (func.lower(Note.title).like(q_clean)) | (func.lower(Note.content).like(q_clean))
            )

        total = base_query.distinct().count()

        # Sorting logic
        if sort_by == "created":
            order_col = Note.created_at.desc()
        elif sort_by == "title":
            order_col = Note.title.asc()
        else:  # default "updated"
            order_col = Note.updated_at.desc()

        ordered_notes = (
            base_query.order_by(Note.pinned.desc(), order_col)
            .offset(offset)
            .limit(limit)
            .all()
        )

        result = []
        for n in ordered_notes:
            tag_names = [t.name for t in n.tags]
            out_cnt = len(n.outgoing_links)
            in_cnt = len(n.incoming_links)
            content_str = n.content or ""
            snippet = content_str[:150] + ("..." if len(content_str) > 150 else "")

            result.append({
                "id": n.id,
                "title": n.title,
                "content_snippet": snippet,
                "tags": tag_names,
                "outgoing_link_count": out_cnt,
                "backlink_count": in_cnt,
                "pinned": bool(n.pinned),
                "created_at": n.created_at,
                "updated_at": n.updated_at,
            })

        return result, total

    def get_all_notes_full(self) -> List[Note]:
        """Fetch all notes with tags and links populated."""
        return self.db.query(Note).all()

    def get_all_note_titles(self) -> List[Tuple[int, str]]:
        """Fetch all note IDs and titles."""
        return self.db.query(Note.id, Note.title).all()

    def find_notes_mentioning_title(self, title: str, exclude_note_id: int) -> List[Note]:
        """Find notes whose content contains the title string (ignoring case)."""
        pattern = f"%{title.strip().lower()}%"
        return (
            self.db.query(Note)
            .filter(
                Note.id != exclude_note_id,
                func.lower(Note.content).like(pattern)
            )
            .all()
        )
