from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.assist_service import AssistService
from app.schemas.assist import (
    TagAssistRequest,
    TagAssistResponse,
    ProofreadRequest,
    ProofreadIssue,
    LinkSuggestionItem,
    DismissSuggestionRequest,
    DismissSuggestionResponse,
    AssistStatusResponse,
)

router = APIRouter(prefix="/assist", tags=["Assist & Intelligence"])

def get_assist_service(db: Session = Depends(get_db)) -> AssistService:
    return AssistService(db)

@router.get("/status", response_model=AssistStatusResponse, operation_id="get_assist_status")
def get_status(service: AssistService = Depends(get_assist_service)):
    """Reports whether AI assistant is enabled and the active provider information."""
    return service.get_status()

@router.post("/tags", response_model=TagAssistResponse, operation_id="assist_tags")
def assist_tags(
    payload: TagAssistRequest,
    service: AssistService = Depends(get_assist_service),
):
    """
    Analyzes note tags: normalizes input, detects phrase merge opportunities,
    typos, and derives smart keyword tag suggestions from note content.
    """
    return service.assist_tags(
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
    )

@router.post("/proofread", response_model=List[ProofreadIssue], operation_id="proofread_content")
def proofread(
    payload: ProofreadRequest,
    service: AssistService = Depends(get_assist_service),
):
    """
    Performs deterministic offline proofreading on note text:
    checks casing, repeated words, and typos while exempting code, wikilinks, and known titles.
    """
    return service.proofread(
        text=payload.text,
        ignored_words=payload.ignored_words,
    )

@router.get("/link-suggestions", response_model=List[LinkSuggestionItem], operation_id="get_link_suggestions")
def get_link_suggestions(
    note_id: int = Query(..., description="ID of the note to retrieve link suggestions for"),
    service: AssistService = Depends(get_assist_service),
):
    """
    Calculates multi-signal link suggestions based on text mentions, TF-IDF similarity,
    shared tags, and mutual neighbours, excluding dismissed or already linked notes.
    """
    return service.get_link_suggestions(note_id)

@router.post("/link-suggestions/dismiss", response_model=DismissSuggestionResponse, operation_id="dismiss_link_suggestion")
def dismiss_link_suggestion(
    payload: DismissSuggestionRequest,
    service: AssistService = Depends(get_assist_service),
):
    """
    Dismisses a link suggestion pair permanently so it never reappears.
    """
    return service.dismiss_link_suggestion(payload.note_id, payload.other_id)
