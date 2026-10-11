from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class LinkCreate(BaseModel):
    target_id: int = Field(..., description="Target note ID to link to", ge=1)

class LinkRead(BaseModel):
    source_id: int
    target_id: int
    origin: str  # 'auto' or 'manual'
    source_title: Optional[str] = None
    target_title: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LinkDeleteResponse(BaseModel):
    source_id: int
    target_id: int
    message: str

class PendingLinkRead(BaseModel):
    source_id: int
    target_title: str

class SuggestedLinkRead(BaseModel):
    target_id: int
    target_title: str
    similarity_score: float
    shared_tags: List[str] = []
