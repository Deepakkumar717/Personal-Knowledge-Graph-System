from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog

class ActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def log(
        self,
        action: str,
        entity: str,
        entity_id: Optional[int] = None,
        title: Optional[str] = None,
        detail: Optional[str] = None,
    ) -> ActivityLog:
        """Record an activity event in the activity log."""
        record = ActivityLog(
            action=action,
            entity=entity,
            entity_id=entity_id,
            title=title,
            detail=detail,
            ts=datetime.now(timezone.utc),
        )
        self.db.add(record)
        # We don't necessarily commit here if called within an outer transaction,
        # but flush so it gets an ID.
        self.db.flush()
        return record

    def get_latest(self, limit: int = 100) -> List[ActivityLog]:
        """Fetch the most recent activity log items."""
        return (
            self.db.query(ActivityLog)
            .order_by(ActivityLog.ts.desc(), ActivityLog.id.desc())
            .limit(limit)
            .all()
        )
