from pydantic import BaseModel, ConfigDict, Field
from typing import List

class TagRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class TagUsage(BaseModel):
    id: int
    name: str
    count: int

class TagSuggestion(BaseModel):
    name: str
    count: int
    score: float

class TagSuggestResponse(BaseModel):
    query: str
    suggestions: List[TagSuggestion]
