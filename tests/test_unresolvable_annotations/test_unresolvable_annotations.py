"""Tests that unresolvable annotations raise clear errors at route registration time.

Covers two common user mistakes:
1. Using a type imported only under `if TYPE_CHECKING:` in endpoint/dependency params.
2. Using a class that is defined after the route that references it.
"""

import importlib

import pytest
from fastapi.testclient import TestClient

APP_PREFIX = "tests.test_unresolvable_annotations.apps"


def test_type_declared_after_endpoint():
    """A class used as an endpoint param before it's defined should fail."""
    with pytest.raises(NameError, match="Could not resolve annotation 'Potato'"):
        importlib.import_module(f"{APP_PREFIX}.type_declared_after_endpoint")


def test_annotated_depends_late_type():
    """Annotated[Potato, Depends(get_potato)] with Potato defined after the route should fail."""
    with pytest.raises(NameError, match="Could not resolve annotation"):
        importlib.import_module(f"{APP_PREFIX}.annotated_depends_late_type")


def test_type_checking_import_in_endpoint_param():
    """TYPE_CHECKING-only import used as an endpoint parameter type should fail."""
    with pytest.raises(NameError, match="Could not resolve annotation 'BaseModel'"):
        importlib.import_module(f"{APP_PREFIX}.type_checking_in_endpoint_param")


def test_type_checking_import_in_dependency_param():
    """TYPE_CHECKING-only import used as a dependency parameter type should fail."""
    with pytest.raises(NameError, match="Could not resolve annotation 'BaseModel'"):
        importlib.import_module(f"{APP_PREFIX}.type_checking_in_dep_param")


def test_type_checking_import_in_return_type():
    """TYPE_CHECKING-only import used as an endpoint return type should fail."""
    with pytest.raises(NameError, match="Could not resolve annotation 'BaseModel'"):
        importlib.import_module(f"{APP_PREFIX}.type_checking_in_return_type")


def test_type_checking_dep_return_type_is_safe():
    """TYPE_CHECKING-only import used ONLY as a dependency return type is safe.

    FastAPI doesn't inspect dependency return types for schema generation,
    so this pattern should not raise an error.
    """
    mod = importlib.import_module(f"{APP_PREFIX}.type_checking_dep_return_type_safe")
    client = TestClient(mod.app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"db": "fake_db"}


def test_valid_type_before_endpoint():
    """Sanity check: a type defined before the route works normally."""
    mod = importlib.import_module(f"{APP_PREFIX}.valid_type_before_endpoint")
    client = TestClient(mod.app)
    response = client.post("/", json={"name": "test"})
    assert response.status_code == 200
    assert response.json() == {"name": "test"}


def test_error_message_mentions_both_causes():
    """The error message should mention both TYPE_CHECKING and late declaration."""
    from fastapi.dependencies.utils import get_typed_annotation

    with pytest.raises(NameError, match="TYPE_CHECKING") as exc_info:
        get_typed_annotation("Unresolvable", {})
    assert "defined after the route" in str(exc_info.value)
