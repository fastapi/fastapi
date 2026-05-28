import pytest
from fastapi.routing import _is_json_content_type


@pytest.mark.parametrize(
    "content_type",
    [
        "application/json",
        "application/JSON",
        "Application/JSON",
        "APPLICATION/JSON",
        "application/json; charset=utf-8",
        "application/json;charset=utf-8",
        "application/json ; charset=utf-8",
        "application/geo+json",
        "application/vnd.api+json",
        "application/vnd.example.api+json",
        "application/vnd.api+json; charset=utf-8",
        " application/json ",
    ],
    ids=[
        "plain",
        "upper-subtype",
        "mixed-case",
        "all-upper",
        "with-charset",
        "charset-no-space",
        "charset-extra-space",
        "geo+json",
        "vnd+json",
        "nested-vnd+json",
        "vnd+json-with-charset",
        "surrounding-whitespace",
    ],
)
def test_json_content_types_accepted(content_type: str) -> None:
    assert _is_json_content_type(content_type) is True


@pytest.mark.parametrize(
    "content_type",
    [
        "text/plain",
        "text/html",
        "multipart/form-data",
        "application/xml",
        "application/octet-stream",
        "application/not-really-json",
        "application/geo+json-seq",
        "application/jsonl",
        "application/x-ndjson",
        "json",
        "",
        "application",
        "/json",
        "application/",
    ],
    ids=[
        "text-plain",
        "text-html",
        "multipart",
        "xml",
        "octet-stream",
        "not-really-json",
        "json-seq",
        "jsonl",
        "ndjson",
        "no-slash",
        "empty",
        "no-subtype",
        "no-maintype",
        "trailing-slash",
    ],
)
def test_non_json_content_types_rejected(content_type: str) -> None:
    assert _is_json_content_type(content_type) is False
