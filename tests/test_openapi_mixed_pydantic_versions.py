from typing import List

from fastapi import FastAPI
from fastapi._compat import may_v1
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .utils import PYDANTIC_V2, needs_py_lt_314, needs_pydanticv2


class AddressV1(may_v1.BaseModel):
    street: str


class UserV1(may_v1.BaseModel):
    name: str
    addresses: List[AddressV1] = []


class AddressV2(BaseModel):
    street: str


class UserV2(BaseModel):
    name: str
    primary_address: AddressV1
    secondary_address: AddressV2 | None = None

    if PYDANTIC_V2:
        # Match the pattern used in other tests to force separate input/output schemas
        model_config = {"json_schema_serialization_defaults_required": True}


def _collect_refs(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from _collect_refs(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _collect_refs(item)


@needs_pydanticv2
@needs_py_lt_314
def test_openapi_mixed_pydantic_models_with_separate_input_output_schemas() -> None:
    app = FastAPI(separate_input_output_schemas=True)

    @app.post("/v1-users/", response_model=UserV1)
    def create_v1_user(
        user: UserV1,
    ) -> UserV1:  # pragma: no cover - behavior tested via OpenAPI
        return user

    @app.post("/v2-users/", response_model=UserV2)
    def create_v2_user(
        user: UserV2,
    ) -> UserV2:  # pragma: no cover - behavior tested via OpenAPI
        return user

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    openapi_schema = response.json()
    schemas = openapi_schema["components"]["schemas"]

    # Ensure both Pydantic v1 and v2 models are present in the components
    user_v1_keys = [name for name in schemas if "UserV1" in name]
    user_v2_keys = [name for name in schemas if "UserV2" in name]
    address_v1_keys = [name for name in schemas if "AddressV1" in name]
    address_v2_keys = [name for name in schemas if "AddressV2" in name]

    assert user_v1_keys, "Expected at least one schema for UserV1 (Pydantic v1 model)."
    assert user_v2_keys, "Expected at least one schema for UserV2 (Pydantic v2 model)."
    assert address_v1_keys, (
        "Expected at least one schema for AddressV1 (Pydantic v1 model)."
    )
    assert address_v2_keys, (
        "Expected at least one schema for AddressV2 (Pydantic v2 model)."
    )

    # Ensure that references in the OpenAPI document point to schemas for both versions
    all_refs = list(_collect_refs(openapi_schema))
    assert any("UserV1" in ref for ref in all_refs), (
        "Expected at least one $ref to a UserV1 schema."
    )
    assert any("UserV2" in ref for ref in all_refs), (
        "Expected at least one $ref to a UserV2 schema."
    )
    assert any("AddressV1" in ref for ref in all_refs), (
        "Expected at least one $ref to an AddressV1 schema."
    )
    assert any("AddressV2" in ref for ref in all_refs), (
        "Expected at least one $ref to an AddressV2 schema."
    )


@needs_pydanticv2
@needs_py_lt_314
def test_openapi_mixed_pydantic_models_without_separate_input_output_schemas() -> None:
    app = FastAPI(separate_input_output_schemas=False)

    @app.post("/v1-users/", response_model=UserV1)
    def create_v1_user(
        user: UserV1,
    ) -> UserV1:  # pragma: no cover - behavior tested via OpenAPI
        return user

    @app.post("/v2-users/", response_model=UserV2)
    def create_v2_user(
        user: UserV2,
    ) -> UserV2:  # pragma: no cover - behavior tested via OpenAPI
        return user

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    openapi_schema = response.json()
    schemas = openapi_schema["components"]["schemas"]

    # Even without separate_input_output_schemas, both versions should be represented
    user_v1_keys = [name for name in schemas if "UserV1" in name]
    user_v2_keys = [name for name in schemas if "UserV2" in name]
    address_v1_keys = [name for name in schemas if "AddressV1" in name]
    address_v2_keys = [name for name in schemas if "AddressV2" in name]

    assert user_v1_keys, "Expected at least one schema for UserV1 (Pydantic v1 model)."
    assert user_v2_keys, "Expected at least one schema for UserV2 (Pydantic v2 model)."
    assert address_v1_keys, (
        "Expected at least one schema for AddressV1 (Pydantic v1 model)."
    )
    assert address_v2_keys, (
        "Expected at least one schema for AddressV2 (Pydantic v2 model)."
    )

    # Check that there are no obviously broken references (all $ref values should target components/schemas)
    all_refs = list(_collect_refs(openapi_schema))
    assert all(ref.startswith("#/components/schemas/") for ref in all_refs), (
        "Found a $ref outside components/schemas."
    )
