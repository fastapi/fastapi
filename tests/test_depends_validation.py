import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


def test_depends_with_called_function():
    """Test that calling a function in Depends() raises a clear error."""

    def get_value():
        return "value"

    with pytest.raises(TypeError) as exc_info:
        app = FastAPI()

        @app.get("/")
        def route(val=Depends(get_value())):  # Wrong: calling the function
            return val

    error_message = str(exc_info.value)
    assert "callable" in error_message.lower()
    assert (
        "Depends(my_function())" in error_message
        or "called the dependency" in error_message
    )


def test_depends_with_nested_depends():
    """Test that nesting Depends raises a clear error."""

    def get_value():
        return "value"

    with pytest.raises(TypeError) as exc_info:
        app = FastAPI()

        @app.get("/")
        def route(val=Depends(Depends(get_value))):  # Wrong: nested Depends
            return val

    error_message = str(exc_info.value)
    assert "nested" in error_message.lower()
    assert "Depends(Depends(" in error_message


def test_depends_with_string():
    """Test that passing a string to Depends raises a clear error."""

    with pytest.raises(TypeError) as exc_info:
        app = FastAPI()

        @app.get("/")
        def route(val=Depends("not_a_function")):  # Wrong: string
            return val

    error_message = str(exc_info.value)
    assert "callable" in error_message.lower()
    assert "str" in error_message


def test_depends_with_dict():
    """Test that passing a dict to Depends raises a clear error."""

    with pytest.raises(TypeError) as exc_info:
        app = FastAPI()

        @app.get("/")
        def route(val=Depends({"key": "value"})):  # Wrong: dict
            return val

    error_message = str(exc_info.value)
    assert "callable" in error_message.lower()
    assert "dict" in error_message


def test_depends_with_correct_usage():
    """Test that correct usage of Depends works fine."""

    def get_value():
        return "correct_value"

    app = FastAPI()

    @app.get("/")
    def route(val: str = Depends(get_value)):  # Correct usage
        return {"value": val}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"value": "correct_value"}


def test_depends_with_callable_class():
    """Test that Depends works with callable classes."""

    class CallableClass:
        def __call__(self):
            return "from_callable_class"

    app = FastAPI()

    @app.get("/")
    def route(val: str = Depends(CallableClass())):  # Correct: callable instance
        return {"value": val}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"value": "from_callable_class"}


def test_depends_with_none():
    """Test that Depends with None works (for sub-dependencies)."""

    app = FastAPI()

    @app.get("/")
    def route(val=Depends(None)):  # Valid for sub-dependencies
        return {"value": "none"}

    # This should not raise an error during app definition
    assert app is not None


def test_error_message_quality():
    """Test that error messages are helpful and specific."""

    def returns_dict():
        return {"data": "value"}

    with pytest.raises(TypeError) as exc_info:
        app = FastAPI()

        @app.get("/")
        def route(val=Depends(returns_dict())):
            return val

    error_message = str(exc_info.value)

    # Check that the error message contains helpful hints
    assert any(
        hint in error_message
        for hint in [
            "✓ Correct",
            "✗ Wrong",
            "called the dependency",
            "function instead of passing it",
        ]
    )
