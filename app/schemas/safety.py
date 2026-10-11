from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class HealthResponse(BaseModel):
    status: str
    service: str
    database_path: str
    backups_count: int

    model_config = ConfigDict(from_attributes=True)

class ResetDatabaseRequest(BaseModel):
    confirm: str = Field(..., description="Confirmation phrase; must be exactly 'DELETE ALL'")

class BackupItem(BaseModel):
    filename: str
    created_at: str
    size_bytes: int

class RestoreBackupRequest(BaseModel):
    filename: str
    confirm: str = Field(..., description="Confirmation phrase; must be exactly 'RESTORE'")

class TrashItem(BaseModel):
    id: int
    original_note_id: int
    title: str
    deleted_at: str

    model_config = ConfigDict(from_attributes=True)

class TrashDetail(BaseModel):
    id: int
    original_note_id: int
    title: str
    deleted_at: str
    payload: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class ActivityLogItem(BaseModel):
    id: int
    ts: str
    action: str
    entity: str
    entity_id: Optional[int] = None
    title: Optional[str] = None
    detail: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
