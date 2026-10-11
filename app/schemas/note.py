from pydantic import BaseModel, ConfigDict, Field, field_serializer
from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.link import LinkRead, SuggestedLinkRead

def serialize_iso_utc(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Unique title of the note")
    content: Optional[str] = Field(default="", max_length=50000, description="Markdown content of the note")
    tags: Optional[List[str]] = Field(default_factory=list, description="List of tags for the note")

class NoteUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Unique title of the note")
    content: Optional[str] = Field(default="", max_length=50000, description="Markdown content of the note")
    tags: Optional[List[str]] = Field(default_factory=list, description="List of tags for the note")

class NotePatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, max_length=50000)
    tags: Optional[List[str]] = None
    pinned: Optional[bool] = None

class NoteListItem(BaseModel):
    id: int
    title: str
    content_snippet: str
    tags: List[str]
    outgoing_link_count: int
    backlink_count: int
    pinned: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, dt: Optional[datetime], _info) -> Optional[str]:
        return serialize_iso_utc(dt)

class NoteBacklinkItem(BaseModel):
    id: int
    title: str
    origin: str  # 'auto' or 'manual'

class RelatedNoteItem(BaseModel):
    id: int
    title: str
    score: float
    shared_tags: List[str] = []

class UnlinkedMentionItem(BaseModel):
    note_id: int
    note_title: str
    snippet: str

class NoteDetail(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    pinned: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    outgoing_links: List[LinkRead]
    backlinks: List[NoteBacklinkItem]
    unresolved_links: List[str]  # titles of unresolved [[...]]
    related_notes: List[RelatedNoteItem]

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, dt: Optional[datetime], _info) -> Optional[str]:
        return serialize_iso_utc(dt)

class NoteDeleteResponse(BaseModel):
    id: int
    title: str
    message: str
