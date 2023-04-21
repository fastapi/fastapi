from __future__ import annotations

import http
import logging

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

router = APIRouter()

app = FastAPI()


@router.get("/no-content", status_code=http.HTTPStatus.NO_CONTENT)
def return_no_content() -> None:
    logging.info("endpoint called")


app.include_router(router)

client = TestClient(app)


def test_no_content():
    response = client.get("/no-content")
    assert response.status_code == http.HTTPStatus.NO_CONTENT, response.text
    assert not response.content
