"""FastAPI routes for the optional local HTTP interface."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from api_orchestrated_agent.orchestrator.agent_loop import AgentOrchestrator

router = APIRouter()


class ProcessRequest(BaseModel):
    text: str = Field(min_length=1)
    source_name: str | None = None


class ProcessResponse(BaseModel):
    result: str


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/process", response_model=ProcessResponse)
def process_request(payload: ProcessRequest) -> ProcessResponse:
    try:
        result = AgentOrchestrator().process_text(payload.text, payload.source_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ProcessResponse(result=result)
