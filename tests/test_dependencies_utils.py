from typing import ForwardRef

import pytest
from fastapi.dependencies.utils import get_typed_annotation


def test_get_typed_annotation():
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    assert typed_annotation is None


def test_get_typed_annotation_unresolvable_string():
    """A string annotation that can't be resolved should raise NameError."""
    with pytest.raises(NameError, match="Could not resolve annotation 'NonExistent'"):
        get_typed_annotation("NonExistent", {})


def test_get_typed_annotation_unresolvable_forward_ref():
    """A ForwardRef that can't be resolved should raise NameError."""
    ref = ForwardRef("UnknownModel")
    with pytest.raises(NameError, match="Could not resolve annotation 'UnknownModel'"):
        get_typed_annotation(ref, {})


def test_get_typed_annotation_resolvable_string():
    """A string annotation that can be resolved should return the type."""
    ns = {"int": int}
    result = get_typed_annotation("int", ns)
    assert result is int


def test_get_typed_annotation_resolvable_forward_ref():
    """A ForwardRef that can be resolved should return the type."""
    ns = {"MyClass": str}
    ref = ForwardRef("MyClass")
    result = get_typed_annotation(ref, ns)
    assert result is str


def test_get_typed_annotation_non_string_passthrough():
    """Non-string, non-ForwardRef annotations pass through unchanged."""
    result = get_typed_annotation(int, {})
    assert result is int
