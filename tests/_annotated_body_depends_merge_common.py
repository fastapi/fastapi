from typing import Any

from fastapi import UploadFile
from pydantic import BaseModel


class BasePayload(BaseModel):
    kind: str


class FooPayload(BasePayload):
    kind: str = "foo"
    extra_foo: str


class BarPayload(BasePayload):
    kind: str = "bar"
    extra_bar: str


class FooFilePayload(BasePayload):
    kind: str = "foo"
    extra_foo: str
    blob: UploadFile


class BarFilePayload(BasePayload):
    kind: str = "bar"
    extra_bar: str
    blob: UploadFile


def openapi_request_body_schema_ref(
    schema: dict[str, Any],
    *,
    path: str,
    method: str = "post",
    content_type: str,
) -> str:
    return schema["paths"][path][method]["requestBody"]["content"][content_type][
        "schema"
    ]["$ref"]
