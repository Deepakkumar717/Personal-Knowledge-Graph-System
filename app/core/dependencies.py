from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.note_repo import NoteRepository
from app.repositories.tag_repo import TagRepository
from app.repositories.link_repo import LinkRepository
from app.repositories.fts_repo import FTSRepository
from app.services.note_service import NoteService
from app.services.link_service import LinkService
from app.services.tag_service import TagService
from app.services.search_service import SearchService
from app.services.graph_service import GraphService
from app.services.io_service import IOService

def get_note_repo(db: Session = Depends(get_db)) -> NoteRepository:
    return NoteRepository(db)

def get_tag_repo(db: Session = Depends(get_db)) -> TagRepository:
    return TagRepository(db)

def get_link_repo(db: Session = Depends(get_db)) -> LinkRepository:
    return LinkRepository(db)

def get_fts_repo(db: Session = Depends(get_db)) -> FTSRepository:
    return FTSRepository(db)

def get_note_service(db: Session = Depends(get_db)) -> NoteService:
    return NoteService(db)

def get_link_service(db: Session = Depends(get_db)) -> LinkService:
    return LinkService(db)

def get_tag_service(db: Session = Depends(get_db)) -> TagService:
    return TagService(db)

def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    return SearchService(db)

def get_graph_service(db: Session = Depends(get_db)) -> GraphService:
    return GraphService(db)

def get_io_service(db: Session = Depends(get_db)) -> IOService:
    return IOService(db)
