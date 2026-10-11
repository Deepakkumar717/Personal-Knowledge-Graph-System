from typing import List, Dict, Optional, Tuple, Set
from collections import defaultdict
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.models.note_tag import NoteTag

class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by normalized name."""
        return self.db.query(Tag).filter(Tag.name == name).first()

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID."""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_or_create(self, name: str) -> Tag:
        """Find tag or create a new one."""
        tag = self.get_by_name(name)
        if not tag:
            tag = Tag(name=name)
            self.db.add(tag)
            self.db.flush()
        return tag

    def set_note_tags(self, note_id: int, tag_names: List[str]) -> List[Tag]:
        """Set all tags for a note, creating missing tags and removing old links."""
        # Delete existing associations
        self.db.query(NoteTag).filter(NoteTag.note_id == note_id).delete()

        tags = []
        for name in tag_names:
            tag = self.get_or_create(name)
            tags.append(tag)
            note_tag = NoteTag(note_id=note_id, tag_id=tag.id)
            self.db.add(note_tag)

        self.db.flush()
        return tags

    def get_note_tags(self, note_id: int) -> List[Tag]:
        """Get all tags assigned to a note."""
        return (
            self.db.query(Tag)
            .join(NoteTag, NoteTag.tag_id == Tag.id)
            .filter(NoteTag.note_id == note_id)
            .all()
        )

    def get_all_tags_with_counts(self) -> List[Tuple[Tag, int]]:
        """Get all tags with note usage counts ordered by count desc, then name asc."""
        sql = text("""
            SELECT tags.id, tags.name, COUNT(note_tags.note_id) AS usage_count
            FROM tags
            LEFT JOIN note_tags ON tags.id = note_tags.tag_id
            GROUP BY tags.id, tags.name
            ORDER BY usage_count DESC, tags.name ASC;
        """)
        rows = self.db.execute(sql).fetchall()
        result = []
        for r in rows:
            tag = Tag(id=r.id, name=r.name)
            result.append((tag, r.usage_count))
        return result

    def get_tag_co_occurrences(self) -> Dict[str, Dict[str, int]]:
        """Compute co-occurrence counts between tags that appear on the same note."""
        sql = text("""
            SELECT nt1.tag_id AS t1_id, t1.name AS t1_name,
                   nt2.tag_id AS t2_id, t2.name AS t2_name,
                   COUNT(nt1.note_id) AS co_count
            FROM note_tags nt1
            JOIN note_tags nt2 ON nt1.note_id = nt2.note_id AND nt1.tag_id != nt2.tag_id
            JOIN tags t1 ON nt1.tag_id = t1.id
            JOIN tags t2 ON nt2.tag_id = t2.id
            GROUP BY nt1.tag_id, nt2.tag_id;
        """)
        rows = self.db.execute(sql).fetchall()
        co_matrix: Dict[str, Dict[str, int]] = defaultdict(dict)
        for r in rows:
            co_matrix[r.t1_name][r.t2_name] = r.co_count
        return co_matrix

    def delete_orphaned_tags(self) -> int:
        """Delete tags that are not associated with any notes."""
        sql = text("""
            DELETE FROM tags
            WHERE id NOT IN (SELECT DISTINCT tag_id FROM note_tags);
        """)
        res = self.db.execute(sql)
        self.db.flush()
        return res.rowcount
