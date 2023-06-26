import pytest
from fastapi.exceptions import FastAPIError


def test_invalid_response_model():
    with pytest.raises(FastAPIError):
        from docs_src.response_model.tutorial003_04 import app

        assert app  # pragma: no cover
