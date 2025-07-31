from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()
client = TestClient(app)


class DataModelWithoutAlias(BaseModel):
    foo: str = Field(...)


@app.get(
    "/without-alias",
    response_model=DataModelWithoutAlias,
)
def without_alias(data: Annotated[DataModelWithoutAlias, Query(...)]):
    return data


def test_openapi_param_name_without_alias():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert (
        openapi_schema["paths"]["/without-alias"]["get"]["parameters"][0]["name"]
        == "foo"
    )
    assert (
        openapi_schema["paths"]["/without-alias"]["get"]["parameters"][0]["in"]
        == "query"
    )
    assert openapi_schema["components"]["schemas"]["DataModelWithoutAlias"][
        "properties"
    ]["foo"] == {"title": "Foo", "type": "string"}


class DataModelWithAlias(BaseModel):
    foo: str = Field(..., alias="bar")


@app.get(
    "/with-alias",
    response_model=DataModelWithAlias,
)
def with_alias(data: Annotated[DataModelWithAlias, Query(...)]):
    return data


def test_openapi_param_name_with_alias():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert (
        openapi_schema["paths"]["/with-alias"]["get"]["parameters"][0]["name"] == "bar"
    )
    assert (
        openapi_schema["paths"]["/with-alias"]["get"]["parameters"][0]["in"] == "query"
    )
    assert openapi_schema["components"]["schemas"]["DataModelWithAlias"]["properties"][
        "bar"
    ] == {"title": "Bar", "type": "string"}


class DataModelWithSerializationAlias(BaseModel):
    foo: str = Field(..., serialization_alias="bar")


@app.get(
    "/with-serialization-alias",
    response_model=DataModelWithSerializationAlias,
)
def with_serialization_alias(
    data: Annotated[DataModelWithSerializationAlias, Query(...)],
):
    return data


def test_openapi_param_name_with_serialization_alias():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert (
        openapi_schema["paths"]["/with-serialization-alias"]["get"]["parameters"][0][
            "name"
        ]
        == "foo"
    )
    assert (
        openapi_schema["paths"]["/with-serialization-alias"]["get"]["parameters"][0][
            "in"
        ]
        == "query"
    )
    assert openapi_schema["components"]["schemas"]["DataModelWithSerializationAlias"][
        "properties"
    ]["bar"] == {"title": "Bar", "type": "string"}


class DataModelWithValidationAlias(BaseModel):
    foo: str = Field(..., validation_alias="bar")


@app.get(
    "/with-validation-alias",
    response_model=DataModelWithValidationAlias,
)
def with_validation_alias(data: Annotated[DataModelWithValidationAlias, Query(...)]):
    return data


def test_openapi_param_name_with_validation_alias():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert (
        openapi_schema["paths"]["/with-validation-alias"]["get"]["parameters"][0][
            "name"
        ]
        == "bar"
    )
    assert (
        openapi_schema["paths"]["/with-validation-alias"]["get"]["parameters"][0]["in"]
        == "query"
    )
    assert openapi_schema["components"]["schemas"]["DataModelWithValidationAlias"][
        "properties"
    ]["foo"] == {"title": "Foo", "type": "string"}


class DataModelWithBothSpecializedAlias(BaseModel):
    foo: str = Field(..., validation_alias="bar", serialization_alias="baz")


@app.get(
    "/with-both-specialized-alias",
    response_model=DataModelWithBothSpecializedAlias,
)
def with_both_specialized_alias(
    data: Annotated[DataModelWithBothSpecializedAlias, Query(...)],
):
    return data


def test_openapi_param_name_with_both_specialized_alias():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert (
        openapi_schema["paths"]["/with-both-specialized-alias"]["get"]["parameters"][0][
            "name"
        ]
        == "bar"
    )
    assert (
        openapi_schema["paths"]["/with-both-specialized-alias"]["get"]["parameters"][0][
            "in"
        ]
        == "query"
    )
    assert openapi_schema["components"]["schemas"]["DataModelWithBothSpecializedAlias"][
        "properties"
    ]["baz"] == {"title": "Baz", "type": "string"}


class DataModelWithAliasAndBothSpecializedAlias(BaseModel):
    foo: str = Field(
        ..., alias="bar", validation_alias="baz", serialization_alias="qux"
    )


@app.get(
    "/with-alias-and-both-specialized-alias",
    response_model=DataModelWithAliasAndBothSpecializedAlias,
)
def with_alias_and_both_specialized_alias(
    data: Annotated[DataModelWithAliasAndBothSpecializedAlias, Query(...)],
):
    return data


def test_openapi_param_name_with_alias_and_both_specialized_alias():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert (
        openapi_schema["paths"]["/with-alias-and-both-specialized-alias"]["get"][
            "parameters"
        ][0]["name"]
        == "baz"
    )
    assert (
        openapi_schema["paths"]["/with-alias-and-both-specialized-alias"]["get"][
            "parameters"
        ][0]["in"]
        == "query"
    )
    assert openapi_schema["components"]["schemas"][
        "DataModelWithAliasAndBothSpecializedAlias"
    ]["properties"]["qux"] == {"title": "Qux", "type": "string"}
