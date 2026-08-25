from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Log Summariser Sandbox")


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody


class SummaryRecord(BaseModel):
    job_status: Literal['queued','running','succeeded','failed']
    summary_text: str | None = None
    error: ErrorBody | None = None


# In-memory store: tenant_id -> summary_id -> SummaryRecord
STORE: dict[str, dict[str, SummaryRecord]] = {}


@app.get(
    "/tenants/{tenant_id}/summaries/{summary_id}",
    response_model=SummaryRecord,
    responses={404: {"model": ErrorResponse}},
)
def get_summary(tenant_id: str, summary_id: str) -> SummaryRecord:
    tenant_bucket = STORE.get(tenant_id)
    if not tenant_bucket:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "summary not found", "details": None},
        )
    record = tenant_bucket.get(summary_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "summary not found", "details": None},
        )
    return record


# Convert FastAPI's HTTPException.detail into the required error envelope.
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    # Only wrap dict details in our standard shape; otherwise keep a minimal message.
    if isinstance(exc.detail, dict) and "code" in exc.detail and "message" in exc.detail:
        body = {"error": {"code": exc.detail["code"], "message": exc.detail["message"], "details": exc.detail.get("details")}}
    else:
        body = {"error": {"code": "http_error", "message": str(exc.detail), "details": None}}
    from starlette.responses import JSONResponse
    return JSONResponse(status_code=exc.status_code, content=body)

