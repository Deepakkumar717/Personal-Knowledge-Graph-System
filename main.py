import asyncio
import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.error_handlers import register_error_handlers
from app.routers import (
    notes_router,
    graph_router,
    tags_router,
    search_router,
    system_router,
    assist_router,
    trash_router,
)
from app.services.backup_service import backup_service

logger = logging.getLogger("uvicorn")

async def periodic_backup_worker():
    """Background task that runs automatic backups on startup and every 30 minutes."""
    # Initial startup backup
    try:
        backup_file = backup_service.create_backup(reason="startup")
        if backup_file:
            print(f"[Backup] Startup backup created: {backup_file}")
    except Exception as e:
        print(f"[Backup] Startup backup failed: {e}")

    # 30-minute interval
    while True:
        await asyncio.sleep(1800)  # 30 minutes
        try:
            bf = backup_service.create_backup(reason="auto_30m")
            if bf:
                print(f"[Backup] Periodic 30m backup created: {bf}")
        except Exception as e:
            print(f"[Backup] Periodic backup error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Log resolved database path at startup
    resolved_db = settings.DATABASE_PATH.resolve()
    print(f"\n=======================================================")
    print(f"[Startup] Resolved DATABASE_PATH: {resolved_db}")
    print(f"=======================================================\n")

    # Start background backup worker
    backup_task = asyncio.create_task(periodic_backup_worker())
    yield
    backup_task.cancel()
    try:
        await backup_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Personal Knowledge Graph API",
    description="Deterministic, rule-based Personal Knowledge Graph backend with SQLite FTS5, graph traversal, data safety, and persistent topic groups.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register standardized error handlers
register_error_handlers(app)

# Mount API routers
app.include_router(notes_router)
app.include_router(graph_router)
app.include_router(tags_router)
app.include_router(search_router)
app.include_router(system_router)
app.include_router(assist_router)
app.include_router(trash_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        reload_excludes=["*.db*", "*.sqlite*", "*wal*", "*shm*", "*.log", ".pytest_cache/*", "frontend/*"],
    )
