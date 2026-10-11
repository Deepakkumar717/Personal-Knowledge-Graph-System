from pydantic import BaseModel, Field
from typing import List, Optional

class SearchResultItem(BaseModel):
    id: int
    title: str
    snippet: str
    tags: List[str]
    score: float
    match_type: str  # "fts" or "fuzzy"

class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[SearchResultItem]

class AutocompleteItem(BaseModel):
    type: str  # "note" or "tag"
    id: Optional[int] = None  # None for tags
    title: str  # Note title or tag name
    score: float

class AutocompleteResponse(BaseModel):
    query: str
    results: List[AutocompleteItem]

class TitleSuggestItem(BaseModel):
    id: int
    title: str

class TitleSuggestResponse(BaseModel):
    query: str
    results: List[TitleSuggestItem]
