from app.routers.notes import router as notes_router
from app.routers.graph import router as graph_router
from app.routers.tags import router as tags_router
from app.routers.search import router as search_router
from app.routers.system import router as system_router
from app.routers.assist import router as assist_router
from app.routers.trash import router as trash_router

__all__ = [
    "notes_router",
    "graph_router",
    "tags_router",
    "search_router",
    "system_router",
    "assist_router",
    "trash_router",
]
