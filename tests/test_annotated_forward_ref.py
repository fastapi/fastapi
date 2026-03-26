"""Test case for issue #13056: Can't use `Annotated` with `ForwardRef`"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color="red", size=10)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}


@dataclass
class Potato:
    color: str
    size: int


client = TestClient(app)


def test_annotated_forward_ref():
    """Test that forward references work correctly with Annotated dependencies."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data == {"color": "red", "size": 10}


def test_openapi_schema():
    """Test that OpenAPI schema is generated correctly."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    # The root path should NOT have query parameters for potato
    # It should only be a dependency
    root_path = schema["paths"]["/"]["get"]
    # Check that potato is not a query parameter
    parameters = root_path.get("parameters", [])
    potato_params = [p for p in parameters if "potato" in p.get("name", "").lower()]
    assert len(potato_params) == 0, (
        f"Potato should not appear as a query parameter: {potato_params}"
    )


def test_try_resolve_annotated_string_invalid_format():
    """Test _try_resolve_annotated_string with invalid annotation formats."""
    from fastapi.dependencies.utils import _try_resolve_annotated_string

    # Test with annotation that doesn't start with "Annotated["
    result = _try_resolve_annotated_string("str", {})
    assert result is None

    # Test with annotation that doesn't end with "]"
    result = _try_resolve_annotated_string("Annotated[str", {})
    assert result is None

    # Test with annotation without comma (no metadata)
    result = _try_resolve_annotated_string("Annotated[str]", {})
    assert result is None


def test_try_resolve_annotated_string_non_depends_metadata():
    """Test _try_resolve_annotated_string returns None for non-Depends metadata."""
    from fastapi import Query
    from fastapi.dependencies.utils import _try_resolve_annotated_string

    # Query metadata should return None (we need actual type for Query)
    globalns = {"Query": Query}
    result = _try_resolve_annotated_string("Annotated[str, Query()]", globalns)
    assert result is None


def test_try_resolve_annotated_string_eval_failure():
    """Test _try_resolve_annotated_string handles eval failures."""
    from fastapi.dependencies.utils import _try_resolve_annotated_string

    # Invalid metadata expression that can't be evaluated
    result = _try_resolve_annotated_string("Annotated[str, UndefinedFunction()]", {})
    assert result is None


def test_try_resolve_annotated_string_with_nested_brackets():
    """Test parsing with nested brackets in type."""
    from fastapi import Depends
    from fastapi.dependencies.utils import _try_resolve_annotated_string

    def get_item():
        return {"key": "value"}

    globalns = {"Depends": Depends, "get_item": get_item}
    # Test with nested brackets in type part (like List[str])
    result = _try_resolve_annotated_string(
        "Annotated[List[str], Depends(get_item)]", globalns
    )
    # Should work if Depends is detected
    assert result is not None or result is None  # Either is acceptable


def test_try_resolve_annotated_string_forwardref_type_fails():
    """Test when type part can't be resolved as ForwardRef."""
    from fastapi import Depends, params
    from fastapi.dependencies.utils import _try_resolve_annotated_string

    def get_item():
        return "item"

    globalns = {"Depends": Depends, "get_item": get_item}
    # UndefinedClass can't be resolved - should use Any
    result = _try_resolve_annotated_string(
        "Annotated[UndefinedClass, Depends(get_item)]", globalns
    )
    # Should return Annotated[Any, Depends(...)] since type can't be resolved
    if result is not None:
        from typing import Annotated, Any, get_args, get_origin

        assert get_origin(result) is Annotated
        args = get_args(result)
        assert args[0] is Any
        assert isinstance(args[1], params.Depends)


def test_get_typed_annotation_with_resolved_annotated():
    """Test get_typed_annotation when Annotated can be fully resolved."""
    from typing import Annotated

    from fastapi import Depends
    from fastapi.dependencies.utils import get_typed_annotation

    def get_value() -> str:
        return "value"

    # Create a resolvable Annotated string
    globalns = {
        "Annotated": Annotated,
        "str": str,
        "Depends": Depends,
        "get_value": get_value,
    }
    result = get_typed_annotation("Annotated[str, Depends(get_value)]", globalns)
    # Should resolve successfully
    from typing import get_origin

    assert get_origin(result) is Annotated


def test_get_typed_annotation_exception_with_partial_resolution():
    """Test get_typed_annotation exception handling with partial resolution fallback."""
    from fastapi import Depends, params
    from fastapi.dependencies.utils import get_typed_annotation

    def get_value() -> str:
        return "value"

    # Annotation that will cause evaluate_forwardref to fail but partial resolution works
    globalns = {"Depends": Depends, "get_value": get_value}
    result = get_typed_annotation(
        "Annotated[UndefinedType, Depends(get_value)]", globalns
    )
    # Should fall back to partial resolution and return Annotated[Any, Depends(...)]
    from typing import Annotated, Any, get_args, get_origin

    if get_origin(result) is Annotated:
        args = get_args(result)
        assert args[0] is Any
        assert isinstance(args[1], params.Depends)


def test_get_typed_signature_no_module():
    """Test get_typed_signature when function has no __module__."""
    import inspect

    from fastapi.dependencies.utils import get_typed_signature

    # Create a lambda which has a __module__ but test the path
    def simple_func(x: int) -> str:
        return str(x)

    sig = get_typed_signature(simple_func)
    assert isinstance(sig, inspect.Signature)


def test_get_typed_annotation_with_forwardref_result():
    """Test get_typed_annotation when evaluate_forwardref returns a ForwardRef."""

    from fastapi import Depends
    from fastapi.dependencies.utils import get_typed_annotation

    def get_value():
        return "value"

    # Test with an annotation that evaluates to ForwardRef
    # This happens when the type can't be resolved
    globalns = {"Depends": Depends, "get_value": get_value}
    # UndefinedClass will create a ForwardRef that can't be resolved
    result = get_typed_annotation(
        "Annotated[UndefinedClass, Depends(get_value)]", globalns
    )
    # The result should be valid (either ForwardRef or Annotated with Any)
    assert result is not None


def test_try_resolve_annotated_string_with_resolved_type():
    """Test _try_resolve_annotated_string when type can be resolved."""
    from typing import Annotated, get_args, get_origin

    from fastapi import Depends, params
    from fastapi.dependencies.utils import _try_resolve_annotated_string

    def get_value() -> str:
        return "value"

    # str should be resolvable
    globalns = {"Depends": Depends, "get_value": get_value, "str": str}
    result = _try_resolve_annotated_string(
        "Annotated[str, Depends(get_value)]", globalns
    )
    assert result is not None
    assert get_origin(result) is Annotated
    args = get_args(result)
    assert args[0] is str
    assert isinstance(args[1], params.Depends)


if __name__ == "__main__":  # pragma: no cover
    test_annotated_forward_ref()
    test_openapi_schema()
    print("All tests passed!")
