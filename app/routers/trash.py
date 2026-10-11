from typing import List
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.trash_service import TrashService
from app.services.event_service import event_service
from app.schemas.safety import TrashItem, TrashDetail
from app.schemas.note import NoteDetail

router = APIRouter(prefix="/trash", tags=["trash"])

def get_trash_service(db: Session = Depends(get_db)) -> TrashService:
    return TrashService(db)

@router.get(
    "/",
    response_model=List[TrashItem],
    summary="List trash items",
    operation_id="list_trash",
)
def list_trash(service: TrashService = Depends(get_trash_service)):
    """List deleted notes currently stored in trash (snapshots kept for 30 days)."""
    return service.list_trash()

@router.get(
    "/{trash_id}",
    response_model=TrashDetail,
    summary="Get trash item details",
    operation_id="get_trash_item",
)
def get_trash_item(
    trash_id: int = Path(..., ge=1),
    service: TrashService = Depends(get_trash_service),
):
    """View details and snapshot payload of a deleted note in trash."""
    return service.get_trash_detail(trash_id)

@router.post(
    "/{trash_id}/restore",
    response_model=NoteDetail,
    summary="Restore note from trash",
    operation_id="restore_note_from_trash",
)
async def restore_note(
    trash_id: int = Path(..., ge=1),
    service: TrashService = Depends(get_trash_service),
):
    """Recreate note from trash snapshot, restoring tags, links, and group. Returns 409 if title is taken."""
    restored = service.restore_note(trash_id)
    await event_service.broadcast("note_created", {"id": restored.id, "title": restored.title})
    return restored

@router.delete(
    "/{trash_id}",
    summary="Permanently delete trash item",
    operation_id="delete_trash_item",
)
def delete_trash_item(
    trash_id: int = Path(..., ge=1),
    service: TrashService = Depends(get_trash_service),
):
    """Permanently delete a note snapshot from trash."""
    service.delete_trash_item(trash_id)
    return {"status": "success", "message": f"Trash item {trash_id} permanently removed."}

@router.delete(
    "/",
    summary="Empty trash",
    operation_id="empty_trash",
)
def empty_trash(service: TrashService = Depends(get_trash_service)):
    """Permanently delete all items from trash."""
    count = service.empty_trash()
    return {"status": "success", "message": f"Emptied trash ({count} items removed)."}
