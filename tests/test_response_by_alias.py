from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class Model(BaseModel):
    name: str = Field(alias="alias")


class ModelNoAlias(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "description": (
                "response_model_by_alias=False is basically a quick hack, to support "
                "proper OpenAPI use another model with the correct field names"
            )
        }


@app.get("/dict", response_model=Model, response_model_by_alias=False)
def read_dict():
    return {"alias": "Foo"}


@app.get("/model", response_model=Model, response_model_by_alias=False)
def read_model():
    return Model(alias="Foo")


@app.get("/list", response_model=List[Model], response_model_by_alias=False)
def read_list():
    return [{"alias": "Foo"}, {"alias": "Bar"}]


@app.get("/by-alias/dict", response_model=Model)
def by_alias_dict():
    return {"alias": "Foo"}


@app.get("/by-alias/model", response_model=Model)
def by_alias_model():
    return Model(alias="Foo")


@app.get("/by-alias/list", response_model=List[Model])
def by_alias_list():
    return [{"alias": "Foo"}, {"alias": "Bar"}]


@app.get("/no-alias/dict", response_model=ModelNoAlias)
def by_alias_dict():
    return {"name": "Foo"}


@app.get("/no-alias/model", response_model=ModelNoAlias)
def by_alias_model():
    return ModelNoAlias(name="Foo")


@app.get("/no-alias/list", response_model=List[ModelNoAlias])
def by_alias_list():
    return [{"name": "Foo"}, {"name": "Bar"}]


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/dict": {
            "get": {
                "summary": "Read Dict",
                "operationId": "read_dict_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Model"}
                            }
                        },
                    }
                },
            }
        },
        "/model": {
            "get": {
                "summary": "Read Model",
                "operationId": "read_model_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Model"}
                            }
                        },
                    }
                },
            }
        },
        "/list": {
            "get": {
                "summary": "Read List",
                "operationId": "read_list_list_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Read List List Get",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Model"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/by-alias/dict": {
            "get": {
                "summary": "By Alias Dict",
                "operationId": "by_alias_dict_by_alias_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Model"}
                            }
                        },
                    }
                },
            }
        },
        "/by-alias/model": {
            "get": {
                "summary": "By Alias Model",
                "operationId": "by_alias_model_by_alias_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Model"}
                            }
                        },
                    }
                },
            }
        },
        "/by-alias/list": {
            "get": {
                "summary": "By Alias List",
                "operationId": "by_alias_list_by_alias_list_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response By Alias List By Alias List Get",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Model"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/no-alias/dict": {
            "get": {
                "summary": "By Alias Dict",
                "operationId": "by_alias_dict_no_alias_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelNoAlias"}
                            }
                        },
                    }
                },
            }
        },
        "/no-alias/model": {
            "get": {
                "summary": "By Alias Model",
                "operationId": "by_alias_model_no_alias_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelNoAlias"}
                            }
                        },
                    }
                },
            }
        },
        "/no-alias/list": {
            "get": {
                "summary": "By Alias List",
                "operationId": "by_alias_list_no_alias_list_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response By Alias List No Alias List Get",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/ModelNoAlias"
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Model": {
                "title": "Model",
                "required": ["alias"],
                "type": "object",
                "properties": {"alias": {"title": "Alias", "type": "string"}},
            },
            "ModelNoAlias": {
                "title": "ModelNoAlias",
                "required": ["name"],
                "type": "object",
                "properties": {"name": {"title": "Name", "type": "string"}},
                "description": "response_model_by_alias=False is basically a quick hack, to support proper OpenAPI use another model with the correct field names",
            },
        }
    },
}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_read_dict():
    response = client.get("/dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_read_model():
    response = client.get("/model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_read_list():
    response = client.get("/list")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "Foo"},
        {"name": "Bar"},
    ]


def test_read_dict_by_alias():
    response = client.get("/by-alias/dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"alias": "Foo"}


def test_read_model_by_alias():
    response = client.get("/by-alias/model")
    assert response.status_code == 200, response.text
    assert response.json() == {"alias": "Foo"}


def test_read_list_by_alias():
    response = client.get("/by-alias/list")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"alias": "Foo"},
        {"alias": "Bar"},
    ]


def test_read_dict_no_alias():
    response = client.get("/no-alias/dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_read_model_no_alias():
    response = client.get("/no-alias/model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_read_list_no_alias():
    response = client.get("/no-alias/list")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "Foo"},
        {"name": "Bar"},
    ]
