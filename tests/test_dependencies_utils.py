import inspect
import sys
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.dependencies.utils import get_typed_annotation, get_typed_signature


def test_get_typed_annotation():
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    assert typed_annotation is None


def test_get_signature_nameerror_py314_branch():
    """Cover _get_signature NameError branch with Python 3.14+ annotation_format path."""
    real_signature = inspect.signature

    def mock_signature(call, *args, **kwargs):
        if kwargs.get("eval_str") is True:
            raise NameError("undefined name")
        # On Python < 3.14, inspect.signature does not accept annotation_format
        kwargs.pop("annotation_format", None)
        return real_signature(call, *args, **kwargs)

    def simple_dep(x: int) -> int:
        return x

    # annotationlib is only available on Python 3.14+; provide a minimal mock  # noqa: E501
    fake_annotationlib = SimpleNamespace(Format=SimpleNamespace(FORWARDREF=object()))

    with (
        patch.object(sys, "version_info", (3, 14)),
        patch.dict("sys.modules", {"annotationlib": fake_annotationlib}),
        patch("fastapi.dependencies.utils.inspect.signature", mock_signature),
    ):
        sig = get_typed_signature(simple_dep)
    assert len(sig.parameters) == 1
    assert sig.parameters["x"].annotation is int
    assert simple_dep(42) == 42  # cover simple_dep body
