from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from app.core.database import Base

class NoteTag(Base):
    __tablename__ = "note_tags"

    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("note_id", "tag_id"),
    )
