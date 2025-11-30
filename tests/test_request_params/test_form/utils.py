from typing import Any, Dict


def get_body_model_name(openapi: Dict[str, Any], path: str) -> str:
    body = openapi["paths"][path]["post"]["requestBody"]
    body_schema = body["content"]["application/x-www-form-urlencoded"]["schema"]
    return body_schema.get("$ref", "").split("/")[-1]
