from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.search import SearchResponse, AutocompleteResponse, TitleSuggestResponse
from app.schemas.link import SuggestedLinkRead
from app.services.search_service import SearchService
from app.services.link_service import LinkService
from app.core.dependencies import get_search_service, get_link_service

router = APIRouter(tags=["search"])

@router.get(
    "/search/",
    response_model=SearchResponse,
    summary="Search notes full-text",
    operation_id="search_notes",
)
def search_notes(
    q: str = Query("", description="Full text search query with support for #tag"),
    tag: Optional[str] = Query(None, description="Tag filter"),
    limit: int = Query(50, ge=1, le=200, description="Max search results"),
    search_service: SearchService = Depends(get_search_service),
):
    """Ranked full-text search using SQLite FTS5 BM25 ranking and fuzzy fallback."""
    return search_service.search(query=q, tag=tag, limit=limit)

@router.get(
    "/search/suggest",
    response_model=AutocompleteResponse,
    summary="Autocomplete suggestions",
    operation_id="autocomplete",
)
def autocomplete(
    q: str = Query(..., min_length=1, description="Autocomplete prefix query"),
    limit: int = Query(10, ge=1, le=50, description="Max items to return"),
    search_service: SearchService = Depends(get_search_service),
):
    """Fast autocomplete ranking title prefix > tag prefix > title substring > fuzzy."""
    return search_service.autocomplete(query=q, limit=limit)

@router.get(
    "/titles/suggest",
    response_model=TitleSuggestResponse,
    summary="Suggest titles for wikilink editor popup",
    operation_id="suggest_titles",
)
def suggest_titles(
    q: str = Query("", description="Title query prefix"),
    limit: int = Query(10, ge=1, le=200, description="Max suggestions"),
    search_service: SearchService = Depends(get_search_service),
):
    """Suggest existing note titles for [[ popup autocomplete during editing."""
    return search_service.suggest_titles_for_wikilink(query=q, limit=limit)

@router.get(
    "/suggest/links",
    response_model=List[SuggestedLinkRead],
    summary="Suggest potential links for note",
    operation_id="suggest_links",
)
def suggest_links(
    note_id: int = Query(..., ge=1, description="Note ID to find suggestions for"),
    limit: int = Query(5, ge=1, le=20, description="Max suggestions"),
    link_service: LinkService = Depends(get_link_service),
):
    """Suggest links based on TF-IDF similarity and shared tags, excluding existing links."""
    return link_service.get_suggested_links(note_id=note_id, limit=limit)
