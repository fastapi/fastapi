from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, FastAPI, Query
from fastapi.testclient import TestClient
from freezegun import freeze_time


def test_include_router_builds_fields_before_first_request():
    router = APIRouter()

    @router.get("/m")
    def handler(from_date: Annotated[Optional[date], Query()] = None):
        return {"from_date": str(from_date)}

    app = FastAPI()
    app.include_router(router, prefix="/api")

    client = TestClient(app, raise_server_exceptions=False)

    with freeze_time("2024-05-13"):
        response = client.get("/api/m")

    assert response.status_code == 200