"""Tests for initialization of FastAPI app instance."""

import pytest
from fastapi import FastAPI


def test_open_api_url_no_title():
    """An error should be raised if an openapi URL is provided without a title."""
    with pytest.raises(ValueError):
        FastAPI(openapi_url="/openapi.json", title=None)


def test_open_api_url_no_version():
    """An error should be raised if an openapi URL is provided without a version."""
    with pytest.raises(ValueError):
        FastAPI(openapi_url="/openapi.json", version=None)


def test_open_api_url_title_and_version():
    """No error should be raised if an openapi URL is provided with a title and version."""
    FastAPI(openapi_url="/openapi.json", title="Title", version="0.1")
