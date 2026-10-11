from sqlalchemy import Column, Integer, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Link(Base):
    __tablename__ = "links"

    source_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    origin = Column(Text, nullable=False, default="manual")

    __table_args__ = (
        PrimaryKeyConstraint("source_id", "target_id"),
    )

    source_note = relationship("Note", foreign_keys=[source_id], back_populates="outgoing_links")
    target_note = relationship("Note", foreign_keys=[target_id], back_populates="incoming_links")
