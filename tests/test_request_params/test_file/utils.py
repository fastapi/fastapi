from typing import Any


def get_body_model_name(openapi: dict[str, Any], path: str) -> str:
    body = openapi["paths"][path]["post"]["requestBody"]
    body_schema = body["content"]["multipart/form-data"]["schema"]
    return body_schema.get("$ref", "").split("/")[-1]
