import json
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.trash import Trash

class TrashRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_snapshot(self, original_note_id: int, title: str, payload: dict) -> Trash:
        """Store a full snapshot of a note prior to deletion."""
        record = Trash(
            original_note_id=original_note_id,
            title=title,
            payload_json=json.dumps(payload),
            deleted_at=datetime.now(timezone.utc),
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_by_id(self, trash_id: int) -> Optional[Trash]:
        return self.db.query(Trash).filter(Trash.id == trash_id).first()

    def list_all(self) -> List[Trash]:
        return self.db.query(Trash).order_by(Trash.deleted_at.desc()).all()

    def delete(self, trash_id: int) -> bool:
        record = self.get_by_id(trash_id)
        if record:
            self.db.delete(record)
            self.db.flush()
            return True
        return False

    def empty_trash(self) -> int:
        count = self.db.query(Trash).delete()
        self.db.flush()
        return count

    def purge_older_than(self, days: int = 30) -> int:
        """Purge trash records older than specified days. NEVER deletes live notes."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        count = self.db.query(Trash).filter(Trash.deleted_at < cutoff).delete()
        self.db.flush()
        return count
