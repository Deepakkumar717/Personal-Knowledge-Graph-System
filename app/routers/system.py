from typing import Dict, Any, List
from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.services.io_service import IOService
from app.services.event_service import event_service
from app.services.backup_service import backup_service
from app.repositories.activity_repo import ActivityRepository
from app.core.dependencies import get_io_service
from app.schemas.safety import (
    HealthResponse,
    ResetDatabaseRequest,
    BackupItem,
    RestoreBackupRequest,
    ActivityLogItem,
)

router = APIRouter(tags=["system"])

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    operation_id="health_check",
)
def health_check():
    """Health check endpoint exposing service status, resolved absolute database path, and backups count."""
    return HealthResponse(
        status="ok",
        service="Personal Knowledge Graph Backend",
        database_path=str(settings.DATABASE_PATH.resolve()),
        backups_count=len(backup_service.list_backups()),
    )

@router.get(
    "/export",
    summary="Export knowledge graph data",
    operation_id="export_graph_data",
)
def export_graph_data(
    io_service: IOService = Depends(get_io_service),
):
    """Export all notes, tags, and links as a JSON file."""
    return io_service.export_data()

@router.post(
    "/import",
    summary="Import knowledge graph data",
    operation_id="import_graph_data",
)
def import_graph_data(
    payload: Dict[str, Any] = Body(..., description="JSON payload containing notes, tags, and links"),
    io_service: IOService = Depends(get_io_service),
):
    """Import notes, tags, and links from a JSON payload."""
    return io_service.import_data(payload)

@router.get(
    "/events",
    summary="Subscribe to SSE events",
    operation_id="events_stream",
)
async def events_stream():
    """Server-Sent Events (SSE) stream broadcasting real-time graph mutations."""
    return StreamingResponse(
        event_service.event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@router.delete(
    "/system/reset",
    summary="Reset database to empty state",
    operation_id="reset_database",
)
async def reset_database(
    payload: ResetDatabaseRequest = Body(..., description="Must contain confirm: 'DELETE ALL'"),
    io_service: IOService = Depends(get_io_service),
):
    """Clear all notes, tags, links, and groups. Requires explicit confirmation 'DELETE ALL'. Takes automatic backup first."""
    if payload.confirm != "DELETE ALL":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Typed confirmation required. Field 'confirm' must equal 'DELETE ALL'.",
        )
    res = io_service.reset_database(confirm=payload.confirm)
    await event_service.broadcast("database_reset", {})
    return res

@router.get(
    "/system/backups",
    response_model=List[BackupItem],
    summary="List database backups",
    operation_id="list_backups",
)
def list_backups():
    """List all available database backup files."""
    return backup_service.list_backups()

@router.post(
    "/system/backups/restore",
    summary="Restore database backup",
    operation_id="restore_backup",
)
async def restore_backup(
    payload: RestoreBackupRequest = Body(...),
    db: Session = Depends(get_db),
):
    """Restores database from specified backup. Requires confirm: 'RESTORE'."""
    if payload.confirm != "RESTORE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Confirmation required. Field 'confirm' must equal 'RESTORE'.",
        )
    try:
        backup_service.restore_backup(payload.filename)
        from app.nlp.tfidf import tfidf_engine
        tfidf_engine.invalidate()
        # Log restore
        activity_repo = ActivityRepository(db)
        activity_repo.log(
            action="restore_backup",
            entity="system",
            title=payload.filename,
            detail=f"Restored database from backup file '{payload.filename}'",
        )
        db.commit()
        await event_service.broadcast("database_reset", {})
        return {"status": "success", "message": f"Successfully restored from '{payload.filename}'."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/system/activity",
    response_model=List[ActivityLogItem],
    summary="Get recent activity log",
    operation_id="get_activity_log",
)
def get_activity_log(
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Fetch recent system activity log items."""
    records = ActivityRepository(db).get_latest(limit=limit)
    return [
        ActivityLogItem(
            id=r.id,
            ts=r.ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            action=r.action,
            entity=r.entity,
            entity_id=r.entity_id,
            title=r.title,
            detail=r.detail,
        )
        for r in records
    ]
