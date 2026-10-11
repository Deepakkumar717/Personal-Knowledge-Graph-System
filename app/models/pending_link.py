from sqlalchemy import Column, Integer, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class PendingLink(Base):
    __tablename__ = "pending_links"

    source_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    target_title_lower = Column(Text, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("source_id", "target_title_lower"),
    )

    source_note = relationship("Note", back_populates="pending_links")
