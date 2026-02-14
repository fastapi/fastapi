"""Test Pydantic validators in Annotated work correctly with FastAPI.

This test ensures that Pydantic v2 validators like AfterValidator, BeforeValidator
work correctly in Annotated types with FastAPI parameters.

Context: PR #13314 broke AfterValidator support and was reverted.
We need to ensure new changes preserve validator functionality.
"""

from typing import Annotated

from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import AfterValidator, BeforeValidator


def validate_positive(v: int) -> int:
    """Validator that ensures value is positive."""
    if v <= 0:
        raise ValueError("must be positive")
    return v


def double_value(v) -> int:
    """Validator that doubles the input value."""
    # BeforeValidator receives the raw value before Pydantic coercion
    # For query params, this is a string
    v_int = int(v) if isinstance(v, str) else v
    return v_int * 2


def strip_whitespace(v: str) -> str:
    """Validator that strips whitespace."""
    return v.strip()


app = FastAPI()


@app.get("/query-after-validator")
def query_after_validator(
    value: Annotated[int, AfterValidator(validate_positive), Query()],
) -> int:
    return value


@app.get("/query-before-validator")
def query_before_validator(
    value: Annotated[int, BeforeValidator(double_value), Query()],
) -> int:
    return value


@app.post("/body-after-validator")
def body_after_validator(
    value: Annotated[int, AfterValidator(validate_positive), Body()],
) -> int:
    return value


@app.post("/body-before-validator")
def body_before_validator(
    name: Annotated[str, BeforeValidator(strip_whitespace), Body()],
) -> str:
    return name


@app.get("/query-multiple-validators")
def query_multiple_validators(
    value: Annotated[
        int,
        BeforeValidator(double_value),
        AfterValidator(validate_positive),
        Query(),
    ],
) -> int:
    return value


client = TestClient(app)


def test_query_after_validator_valid():
    """Test AfterValidator in Query with valid value."""
    response = client.get("/query-after-validator?value=5")
    assert response.status_code == 200, response.text
    assert response.json() == 5


def test_query_after_validator_invalid():
    """Test AfterValidator in Query with invalid value."""
    response = client.get("/query-after-validator?value=-1")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["query", "value"],
                "msg": "Value error, must be positive",
                "input": "-1",
                "ctx": {"error": {}},
            }
        ]
    }


def test_query_before_validator():
    """Test BeforeValidator in Query doubles the value."""
    response = client.get("/query-before-validator?value=5")
    assert response.status_code == 200, response.text
    assert response.json() == 10  # 5 * 2


def test_body_after_validator_valid():
    """Test AfterValidator in Body with valid value."""
    # Body() without embed means send the value directly, not wrapped in an object
    response = client.post("/body-after-validator", json=10)
    assert response.status_code == 200, response.text
    assert response.json() == 10


def test_body_after_validator_invalid():
    """Test AfterValidator in Body with invalid value."""
    response = client.post("/body-after-validator", json=-5)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body"],
                "msg": "Value error, must be positive",
                "input": -5,
                "ctx": {"error": {}},
            }
        ]
    }


def test_body_before_validator():
    """Test BeforeValidator in Body strips whitespace."""
    response = client.post("/body-before-validator", json="  hello  ")
    assert response.status_code == 200, response.text
    assert response.json() == "hello"


def test_query_multiple_validators():
    """Test multiple validators work in correct order."""
    # Input: 3 → BeforeValidator doubles to 6 → AfterValidator checks positive
    response = client.get("/query-multiple-validators?value=3")
    assert response.status_code == 200, response.text
    assert response.json() == 6

    # Input: -1 → BeforeValidator doubles to -2 → AfterValidator fails
    response = client.get("/query-multiple-validators?value=-1")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["query", "value"],
                "msg": "Value error, must be positive",
                "input": "-1",
                "ctx": {"error": {}},
            }
        ]
    }


def test_query_multiple_validators_zero():
    """Test multiple validators with zero (edge case)."""
    # Input: 0 → BeforeValidator doubles to 0 → AfterValidator fails (not positive)
    response = client.get("/query-multiple-validators?value=0")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["query", "value"],
                "msg": "Value error, must be positive",
                "input": "0",
                "ctx": {"error": {}},
            }
        ]
    }
