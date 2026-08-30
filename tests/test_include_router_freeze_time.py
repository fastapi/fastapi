from datetime import date
from typing import Annotated, cast

from fastapi import APIRouter, FastAPI, Query
from fastapi.routing import _IncludedRouter


def test_include_router_builds_fields_before_first_request():
    router = APIRouter()

    @router.get("/m")
    def handler(from_date: Annotated[date | None, Query()] = None):
        return {"from_date": str(from_date)}

    app = FastAPI()
    app.include_router(router, prefix="/api")

    included_router = cast(_IncludedRouter, app.router.routes[-1])

    assert included_router._effective_candidates
