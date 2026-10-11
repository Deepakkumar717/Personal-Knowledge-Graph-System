from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.tag import TagUsage, TagSuggestResponse
from app.services.tag_service import TagService
from app.core.dependencies import get_tag_service

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get(
    "/",
    response_model=List[TagUsage],
    summary="List all tags",
    operation_id="list_tags",
)
def list_tags(
    tag_service: TagService = Depends(get_tag_service),
):
    """List all tags in the system ordered by usage count."""
    return tag_service.list_all_tags()

@router.get(
    "/suggest",
    response_model=TagSuggestResponse,
    summary="Suggest tags",
    operation_id="suggest_tags",
)
def suggest_tags(
    q: str = Query("", description="Tag prefix or search term"),
    selected: Optional[List[str]] = Query(None, description="Currently selected tags for co-occurrence boost"),
    content: Optional[str] = Query(None, description="Optional note text for keyword matching"),
    limit: int = Query(10, ge=1, le=50, description="Max suggestions"),
    tag_service: TagService = Depends(get_tag_service),
):
    """Suggest tags based on query prefix, fuzzy match, popularity, co-occurrence, and note content."""
    return tag_service.suggest_tags(query=q, selected_tags=selected, note_content=content, limit=limit)
