from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class CustomHeaderModel(BaseModel):
    custom_auth: str = Field(alias="X-Custom-Auth")
    validation_key: str = Field(validation_alias="X-Validation-Key")
    user_agent: str

    model_config = {"extra": "forbid"}


@app.get("/test-header-alias")
async def get_header_alias(headers: Annotated[CustomHeaderModel, Header()]):
    return {
        "custom_auth": headers.custom_auth,
        "validation_key": headers.validation_key,
        "user_agent": headers.user_agent,
    }


client = TestClient(app)


def test_header_model_custom_aliases():
    response = client.get(
        "/test-header-alias",
        headers={
            "X-Custom-Auth": "secret123",
            "X-Validation-Key": "key456",
            "User-Agent": "test-client",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["custom_auth"] == "secret123"
    assert data["validation_key"] == "key456"
    assert data["user_agent"] == "test-client"


def test_header_model_underscores_and_alias():
    response = client.get(
        "/test-header-alias",
        headers={
            "x-custom-auth": "secret123",
            "x-validation-key": "key456",
            "user-agent": "test-client",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["custom_auth"] == "secret123"
    assert data["validation_key"] == "key456"
    assert data["user_agent"] == "test-client"
