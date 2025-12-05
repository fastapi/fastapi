"""Tests for __str__ methods of validation exceptions."""

from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
    WebSocketRequestValidationError,
)


def test_request_validation_error_str_single_error():
    """Test string representation of RequestValidationError with single error."""
    errors = [
        {
            "type": "int_parsing",
            "loc": ["query", "id"],
            "msg": "Input should be a valid integer",
        }
    ]
    exc = RequestValidationError(errors)
    result = str(exc)

    assert "1 validation error for request:" in result
    assert "{'type': 'int_parsing'" in result


def test_request_validation_error_str_multiple_errors():
    """Test string representation of RequestValidationError with multiple errors."""
    errors = [
        {
            "type": "int_parsing",
            "loc": ["query", "id"],
            "msg": "Input should be a valid integer",
        },
        {"type": "missing", "loc": ["query", "name"], "msg": "Field required"},
    ]
    exc = RequestValidationError(errors)
    result = str(exc)

    assert "2 validation errors for request:" in result
    assert "int_parsing" in result
    assert "missing" in result


def test_websocket_request_validation_error_str_single_error():
    """Test string representation of WebSocketRequestValidationError with single error."""
    errors = [
        {
            "type": "int_parsing",
            "loc": ["query", "id"],
            "msg": "Input should be a valid integer",
        }
    ]
    exc = WebSocketRequestValidationError(errors)
    result = str(exc)

    assert "1 validation error for WebSocket request:" in result
    assert "{'type': 'int_parsing'" in result


def test_websocket_request_validation_error_str_multiple_errors():
    """Test string representation of WebSocketRequestValidationError with multiple errors."""
    errors = [
        {
            "type": "int_parsing",
            "loc": ["query", "id"],
            "msg": "Input should be a valid integer",
        },
        {"type": "missing", "loc": ["query", "name"], "msg": "Field required"},
    ]
    exc = WebSocketRequestValidationError(errors)
    result = str(exc)

    assert "2 validation errors for WebSocket request:" in result
    assert "int_parsing" in result
    assert "missing" in result


def test_response_validation_error_str_consistency():
    """Test that ResponseValidationError has similar __str__ behavior."""
    errors = [
        {
            "type": "int_parsing",
            "loc": ["response", "id"],
            "msg": "Input should be a valid integer",
        }
    ]
    exc = ResponseValidationError(errors)
    result = str(exc)

    assert "1 validation error" in result
    assert "{'type': 'int_parsing'" in result
