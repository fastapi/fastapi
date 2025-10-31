import pytest
from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.openapi.constants import REF_TEMPLATE
from fastapi.openapi.utils import get_openapi

if PYDANTIC_V2:
    from fastapi._compat.v2 import GenerateJsonSchema
else:
    from fastapi._compat.v1 import GenerateJsonSchema  # type: ignore[assignment]


app = FastAPI()


@app.get("/")
def read_root():
    pass  # pragma: no cover


# Custom schema generator that does nothing but tracks if it was called
class CustomJsonSchemaGenerator(GenerateJsonSchema):
    def __init__(self):
        super().__init__(ref_template=REF_TEMPLATE)
        self.called = False

    def generate_definitions(self, *args, **kwargs):
        self.called = True
        return super().generate_definitions(*args, **kwargs)


def test_custom_schema_generator_called():
    custom_schema_generator = CustomJsonSchemaGenerator()
    get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        schema_generator=custom_schema_generator,
    )

    if PYDANTIC_V2:
        assert custom_schema_generator.called is True
    else:
        assert (  # Pydantic v1 does not use custom schema generators
            custom_schema_generator.called is False
        )


@pytest.mark.parametrize("use_custom_schema_generator", [True, False])
def test_custom_schema_generator_openapi(use_custom_schema_generator: bool):
    custom_schema_generator = (
        CustomJsonSchemaGenerator() if use_custom_schema_generator else None
    )
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        schema_generator=custom_schema_generator,
    )

    assert openapi == OPENAPI_SCHEMA


OPENAPI_SCHEMA = {
    "info": {
        "title": "FastAPI",
        "version": "0.1.0",
    },
    "openapi": "3.1.0",
    "paths": {
        "/": {
            "get": {
                "operationId": "read_root__get",
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {},
                            },
                        },
                        "description": "Successful Response",
                    },
                },
                "summary": "Read Root",
            },
        },
    },
}
