from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.core.database import Base

class DismissedSuggestion(Base):
    __tablename__ = "dismissed_suggestions"

    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    other_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
