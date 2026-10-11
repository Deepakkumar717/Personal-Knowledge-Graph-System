from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, DateTime
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Trash(Base):
    __tablename__ = "trash"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_note_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    payload_json = Column(Text, nullable=False)
    deleted_at = Column(DateTime, default=utc_now, nullable=False)
