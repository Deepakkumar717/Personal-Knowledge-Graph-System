from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False, unique=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pinned = Column(Integer, default=0)

    # Relationships
    tags = relationship("Tag", secondary="note_tags", back_populates="notes", lazy="selectin")
    outgoing_links = relationship(
        "Link",
        foreign_keys="Link.source_id",
        back_populates="source_note",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    incoming_links = relationship(
        "Link",
        foreign_keys="Link.target_id",
        back_populates="target_note",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    pending_links = relationship(
        "PendingLink",
        foreign_keys="PendingLink.source_id",
        back_populates="source_note",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
