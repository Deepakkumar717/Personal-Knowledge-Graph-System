from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# Tag Intelligence Schemas
class TagAssistRequest(BaseModel):
    title: Optional[str] = ""
    content: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)

class TagSuggestionItem(BaseModel):
    tag: str
    reason: str

class PhraseMergeItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    from_tags: List[str] = Field(..., alias="from")
    to_tag: str = Field(..., alias="to")

class TagCorrectionItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    from_tag: str = Field(..., alias="from")
    to_tag: str = Field(..., alias="to")

class TagAssistResponse(BaseModel):
    normalized: List[str]
    suggestions: List[TagSuggestionItem]
    merges: List[PhraseMergeItem]
    corrections: List[TagCorrectionItem]


# Content Proofreading Schemas
class ProofreadRequest(BaseModel):
    text: str
    ignored_words: Optional[List[str]] = Field(default_factory=list)

class ProofreadIssue(BaseModel):
    start: int
    end: int
    original: str
    suggestion: str
    reason: str


# Link Suggestions Schemas
class LinkSuggestionItem(BaseModel):
    note_id: int
    title: str
    score: float
    reasons: List[str]

class DismissSuggestionRequest(BaseModel):
    note_id: int
    other_id: int

class DismissSuggestionResponse(BaseModel):
    status: str
    message: str


# Status Schema
class AssistStatusResponse(BaseModel):
    enabled: bool
    provider: str
    model: Optional[str] = None
