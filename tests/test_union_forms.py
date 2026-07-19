from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel

app = FastAPI()


class UserForm(BaseModel):
    name: str
    email: str


class CompanyForm(BaseModel):
    company_name: str
    industry: str


@app.post("/form-union/")
def post_union_form(data: Annotated[UserForm | CompanyForm, Form()]):
    return {"received": data}


@app.post("/form-optional-required/")
def post_optional_required_form(data: Annotated[UserForm | None, Form()]):
    return {"received": data}


@app.post("/form-optional/")
def post_optional_form(data: Annotated[UserForm | None, Form()] = None):
    return {"received": data}


@app.post("/form-optional-union/")
def post_optional_union_form(
    data: Annotated[UserForm | CompanyForm | None, Form()] = None,
):
    return {"received": data}


client = TestClient(app)


def test_post_user_form():
    response = client.post(
        "/form-union/", data={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "received": {"name": "John Doe", "email": "john@example.com"}
    }


def test_post_company_form():
    response = client.post(
        "/form-union/", data={"company_name": "Tech Corp", "industry": "Technology"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "received": {"company_name": "Tech Corp", "industry": "Technology"}
    }


def test_invalid_form_data():
    response = client.post(
        "/form-union/",
        data={"name": "John", "company_name": "Tech Corp"},
    )
    assert response.status_code == 422, response.text


def test_empty_form():
    response = client.post("/form-union/")
    assert response.status_code == 422, response.text


def test_post_optional_required_form():
    # `UserForm | None` without a default is still required, but its top-level
    # fields must be collected into the model instead of being silently dropped.
    response = client.post(
        "/form-optional-required/",
        data={"name": "John Doe", "email": "john@example.com"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "received": {"name": "John Doe", "email": "john@example.com"}
    }


def test_post_optional_required_form_missing():
    response = client.post("/form-optional-required/")
    assert response.status_code == 422, response.text


def test_post_optional_form():
    # `UserForm | None = None`: submitted fields must still populate the model
    # (previously they were silently discarded and the value resolved to `None`).
    response = client.post(
        "/form-optional/", data={"name": "Jane Doe", "email": "jane@example.com"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "received": {"name": "Jane Doe", "email": "jane@example.com"}
    }


def test_post_optional_form_empty():
    # An empty form is equivalent to an empty object (`{}`), so the required model
    # fields are still validated (mirroring a JSON `{}` body), giving a 422.
    response = client.post("/form-optional/")
    assert response.status_code == 422, response.text


def test_post_optional_union_form():
    response = client.post(
        "/form-optional-union/",
        data={"company_name": "Tech Corp", "industry": "Technology"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "received": {"company_name": "Tech Corp", "industry": "Technology"}
    }


def test_post_optional_union_form_empty():
    # As above, an empty form validates the (required) members, so it is a 422
    # rather than silently resolving to the `None` default.
    response = client.post("/form-optional-union/")
    assert response.status_code == 422, response.text


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/form-union/": {
                    "post": {
                        "summary": "Post Union Form",
                        "operationId": "post_union_form_form_union__post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/UserForm"},
                                            {
                                                "$ref": "#/components/schemas/CompanyForm"
                                            },
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/form-optional-required/": {
                    "post": {
                        "summary": "Post Optional Required Form",
                        "operationId": "post_optional_required_form_form_optional_required__post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/UserForm"},
                                            {"type": "null"},
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/form-optional/": {
                    "post": {
                        "summary": "Post Optional Form",
                        "operationId": "post_optional_form_form_optional__post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/UserForm"},
                                            {"type": "null"},
                                        ],
                                        "title": "Data",
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/form-optional-union/": {
                    "post": {
                        "summary": "Post Optional Union Form",
                        "operationId": "post_optional_union_form_form_optional_union__post",
                        "requestBody": {
                            "content": {
                                "application/x-www-form-urlencoded": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/UserForm"},
                                            {
                                                "$ref": "#/components/schemas/CompanyForm"
                                            },
                                            {"type": "null"},
                                        ],
                                        "title": "Data",
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "CompanyForm": {
                        "properties": {
                            "company_name": {"type": "string", "title": "Company Name"},
                            "industry": {"type": "string", "title": "Industry"},
                        },
                        "type": "object",
                        "required": ["company_name", "industry"],
                        "title": "CompanyForm",
                    },
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "UserForm": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "email": {"type": "string", "title": "Email"},
                        },
                        "type": "object",
                        "required": ["name", "email"],
                        "title": "UserForm",
                    },
                    "ValidationError": {
                        "properties": {
                            "ctx": {"title": "Context", "type": "object"},
                            "input": {"title": "Input"},
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
