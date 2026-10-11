from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, status
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NotePatch,
    NoteListItem,
    NoteDetail,
    NoteBacklinkItem,
    RelatedNoteItem,
    UnlinkedMentionItem,
    NoteDeleteResponse,
)
from app.schemas.link import LinkCreate, LinkRead, LinkDeleteResponse
from app.services.note_service import NoteService
from app.services.link_service import LinkService
from app.services.event_service import event_service
from app.core.dependencies import get_note_service, get_link_service

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post(
    "/",
    response_model=NoteDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    operation_id="create_note",
)
async def create_note(
    payload: NoteCreate,
    note_service: NoteService = Depends(get_note_service),
):
    """Create a new note with title, markdown content, and optional tags."""
    detail = note_service.create_note(payload)
    await event_service.broadcast("note_created", {"id": detail.id, "title": detail.title})
    return detail

@router.get(
    "/",
    response_model=List[NoteListItem],
    summary="List notes",
    operation_id="list_notes",
)
def list_notes(
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    q: Optional[str] = Query(None, description="Search query string in title or content"),
    limit: int = Query(50, ge=1, le=200, description="Max items to return (1-200)"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    sort: str = Query("updated", pattern="^(updated|created|title|links)$", description="Sort order"),
    pinned: Optional[bool] = Query(None, description="Filter by pinned status"),
    note_service: NoteService = Depends(get_note_service),
):
    """List notes with filtering by tag, query, sorting, and pagination."""
    return note_service.list_notes(
        tag=tag, q=q, limit=limit, offset=offset, sort=sort, pinned=pinned
    )

@router.get(
    "/{note_id}",
    response_model=NoteDetail,
    summary="Get note details",
    operation_id="get_note",
)
def get_note(
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    note_service: NoteService = Depends(get_note_service),
):
    """Get full details of a note including outgoing links, backlinks, unresolved links, and related notes."""
    return note_service.get_note_detail(note_id)

@router.put(
    "/{note_id}",
    response_model=NoteDetail,
    summary="Update a note",
    operation_id="update_note",
)
async def update_note(
    payload: NoteUpdate,
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    note_service: NoteService = Depends(get_note_service),
):
    """Full update of note title, content, and tags."""
    detail = note_service.update_note(note_id, payload)
    await event_service.broadcast("note_updated", {"id": detail.id, "title": detail.title})
    return detail

@router.patch(
    "/{note_id}",
    response_model=NoteDetail,
    summary="Partial update a note",
    operation_id="patch_note",
)
async def patch_note(
    payload: NotePatch,
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    note_service: NoteService = Depends(get_note_service),
):
    """Partial update of note fields such as title, content, tags, or pinned state."""
    detail = note_service.patch_note(note_id, payload)
    await event_service.broadcast("note_updated", {"id": detail.id, "title": detail.title})
    return detail

@router.delete(
    "/{note_id}",
    response_model=NoteDeleteResponse,
    summary="Delete a note",
    operation_id="delete_note",
)
async def delete_note(
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    note_service: NoteService = Depends(get_note_service),
):
    """Delete a note and cascade its links and tags."""
    res = note_service.delete_note(note_id)
    await event_service.broadcast("note_deleted", {"id": note_id, "title": res.title})
    return res

@router.patch(
    "/{note_id}/link",
    response_model=LinkRead,
    summary="Create manual link",
    operation_id="link_notes",
)
async def link_notes(
    payload: LinkCreate,
    note_id: int = Path(..., ge=1, description="Positive integer source note ID"),
    link_service: LinkService = Depends(get_link_service),
):
    """Create a manual directed link from source note to target note."""
    link = link_service.create_manual_link(source_id=note_id, target_id=payload.target_id)
    await event_service.broadcast("link_created", {"source_id": note_id, "target_id": payload.target_id})
    return link

@router.delete(
    "/{note_id}/link/{target_id}",
    response_model=LinkDeleteResponse,
    summary="Remove a link",
    operation_id="unlink_notes",
)
async def unlink_notes(
    note_id: int = Path(..., ge=1, description="Positive integer source note ID"),
    target_id: int = Path(..., ge=1, description="Positive integer target note ID"),
    link_service: LinkService = Depends(get_link_service),
):
    """Remove a link between source note and target note."""
    res = link_service.delete_link(source_id=note_id, target_id=target_id)
    await event_service.broadcast("link_deleted", {"source_id": note_id, "target_id": target_id})
    return res

@router.get(
    "/{note_id}/backlinks",
    response_model=List[NoteBacklinkItem],
    summary="Get backlinks for note",
    operation_id="get_note_backlinks",
)
def get_note_backlinks(
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    note_service: NoteService = Depends(get_note_service),
):
    """Get all incoming backlinks pointing to this note."""
    return note_service.get_backlinks(note_id)

@router.get(
    "/{note_id}/related",
    response_model=List[RelatedNoteItem],
    summary="Get related notes",
    operation_id="get_note_related",
)
def get_note_related(
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    limit: int = Query(5, ge=1, le=20, description="Max items to return"),
    note_service: NoteService = Depends(get_note_service),
):
    """Get TF-IDF and tag-similarity related notes."""
    return note_service.get_related_notes(note_id, limit=limit)

@router.get(
    "/{note_id}/mentions",
    response_model=List[UnlinkedMentionItem],
    summary="Get unlinked mentions",
    operation_id="get_note_mentions",
)
def get_note_mentions(
    note_id: int = Path(..., ge=1, description="Positive integer note ID"),
    note_service: NoteService = Depends(get_note_service),
):
    """Get unlinked mentions of this note title in other notes."""
    return note_service.get_unlinked_mentions(note_id)
