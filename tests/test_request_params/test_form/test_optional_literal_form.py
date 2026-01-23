from typing import Annotated, Literal, Optional

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient


def test_optional_literal_form_none():
    """Test that omitting an optional form field returns None"""
    app = FastAPI()

    @app.post("/")
    async def read_main(attribute: Annotated[Optional[Literal["abc", "def"]], Form()]):
        return {"attribute": attribute}

    client = TestClient(app)

    # FIXED: Use empty data instead of {"attribute": None}
    response = client.post("/", data={})
    assert response.status_code == 200
    assert response.json() == {"attribute": None}


def test_optional_literal_form_valid_values():
    """Test that valid literal values work correctly"""
    app = FastAPI()

    @app.post("/")
    async def read_main(attribute: Annotated[Optional[Literal["abc", "def"]], Form()]):
        return {"attribute": attribute}

    client = TestClient(app)

    # Test with "abc"
    response = client.post("/", data={"attribute": "abc"})
    assert response.status_code == 200
    assert response.json() == {"attribute": "abc"}

    # Test with "def"
    response = client.post("/", data={"attribute": "def"})
    assert response.status_code == 200
    assert response.json() == {"attribute": "def"}


def test_optional_literal_form_invalid_value():
    """Test that invalid values return 422"""
    app = FastAPI()

    @app.post("/")
    async def read_main(attribute: Annotated[Optional[Literal["abc", "def"]], Form()]):
        return {"attribute": attribute}

    client = TestClient(app)

    # Invalid value should fail
    response = client.post("/", data={"attribute": "xyz"})
    assert response.status_code == 422

    # String "None" is also invalid
    response = client.post("/", data={"attribute": "None"})
    assert response.status_code == 422


def test_optional_literal_form_empty_string():
    """Test that empty string is treated as None for optional Form fields"""
    app = FastAPI()

    @app.post("/")
    async def read_main(attribute: Annotated[Optional[Literal["abc", "def"]], Form()]):
        return {"attribute": attribute}

    client = TestClient(app)

    # Empty string is treated as "not provided" for optional Form fields
    # This is consistent with FastAPI's behavior for Form data
    response = client.post("/", data={"attribute": ""})
    assert response.status_code == 200
    assert response.json() == {"attribute": None}
