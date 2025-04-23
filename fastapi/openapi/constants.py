from typing import Annotated, Literal

METHODS_WITH_BODY = {"GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"}
REF_PREFIX = "#/components/schemas/"
REF_TEMPLATE = "#/components/schemas/{model}"


TypeValue = Annotated[
    Literal["array", "boolean", "integer", "null", "number", "object", "string"],
    "Allowed type values of an object as specified in the JSON Schema https://json-schema.org/draft/2020-12/json-schema-validation#section-6.1.1",
]
