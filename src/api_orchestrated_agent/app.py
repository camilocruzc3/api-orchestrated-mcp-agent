"""FastAPI application entry point."""
from fastapi import FastAPI

from api_orchestrated_agent.api.routes import router

app = FastAPI(
    title="API-Orchestrated MCP Agent",
    version="0.2.0",
    description="Local API for a programmatic MCP agent with deterministic policies.",
)
app.include_router(router)
