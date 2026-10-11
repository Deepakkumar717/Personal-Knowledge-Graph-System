from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(DateTime, default=utc_now, nullable=False)
    action = Column(String(50), nullable=False)
    entity = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    title = Column(Text, nullable=True)
    detail = Column(Text, nullable=True)
