from typing import List, Union

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError


class BaseUser(BaseModel):
    name: str


class User(BaseUser):
    surname: str


class DBUser(User):
    password_hash: str


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get("/no_response_model-no_annotation-return_model")
def no_response_model_no_annotation_return_model():
    return User(name="John", surname="Doe")


@app.get("/no_response_model-no_annotation-return_dict")
def no_response_model_no_annotation_return_dict():
    return {"name": "John", "surname": "Doe"}


@app.get("/response_model-no_annotation-return_same_model", response_model=User)
def response_model_no_annotation_return_same_model():
    return User(name="John", surname="Doe")


@app.get("/response_model-no_annotation-return_exact_dict", response_model=User)
def response_model_no_annotation_return_exact_dict():
    return {"name": "John", "surname": "Doe"}


@app.get("/response_model-no_annotation-return_invalid_dict", response_model=User)
def response_model_no_annotation_return_invalid_dict():
    return {"name": "John"}


@app.get("/response_model-no_annotation-return_invalid_model", response_model=User)
def response_model_no_annotation_return_invalid_model():
    return Item(name="Foo", price=42.0)


@app.get(
    "/response_model-no_annotation-return_dict_with_extra_data", response_model=User
)
def response_model_no_annotation_return_dict_with_extra_data():
    return {"name": "John", "surname": "Doe", "password_hash": "secret"}


@app.get(
    "/response_model-no_annotation-return_submodel_with_extra_data", response_model=User
)
def response_model_no_annotation_return_submodel_with_extra_data():
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get("/no_response_model-annotation-return_same_model")
def no_response_model_annotation_return_same_model() -> User:
    return User(name="John", surname="Doe")


@app.get("/no_response_model-annotation-return_exact_dict")
def no_response_model_annotation_return_exact_dict() -> User:
    return {"name": "John", "surname": "Doe"}


@app.get("/no_response_model-annotation-return_invalid_dict")
def no_response_model_annotation_return_invalid_dict() -> User:
    return {"name": "John"}


@app.get("/no_response_model-annotation-return_invalid_model")
def no_response_model_annotation_return_invalid_model() -> User:
    return Item(name="Foo", price=42.0)


@app.get("/no_response_model-annotation-return_dict_with_extra_data")
def no_response_model_annotation_return_dict_with_extra_data() -> User:
    return {"name": "John", "surname": "Doe", "password_hash": "secret"}


@app.get("/no_response_model-annotation-return_submodel_with_extra_data")
def no_response_model_annotation_return_submodel_with_extra_data() -> User:
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get("/response_model_none-annotation-return_same_model", response_model=None)
def response_model_none_annotation_return_same_model() -> User:
    return User(name="John", surname="Doe")


@app.get("/response_model_none-annotation-return_exact_dict", response_model=None)
def response_model_none_annotation_return_exact_dict() -> User:
    return {"name": "John", "surname": "Doe"}


@app.get("/response_model_none-annotation-return_invalid_dict", response_model=None)
def response_model_none_annotation_return_invalid_dict() -> User:
    return {"name": "John"}


@app.get("/response_model_none-annotation-return_invalid_model", response_model=None)
def response_model_none_annotation_return_invalid_model() -> User:
    return Item(name="Foo", price=42.0)


@app.get(
    "/response_model_none-annotation-return_dict_with_extra_data", response_model=None
)
def response_model_none_annotation_return_dict_with_extra_data() -> User:
    return {"name": "John", "surname": "Doe", "password_hash": "secret"}


@app.get(
    "/response_model_none-annotation-return_submodel_with_extra_data",
    response_model=None,
)
def response_model_none_annotation_return_submodel_with_extra_data() -> User:
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get(
    "/response_model_model1-annotation_model2-return_same_model", response_model=User
)
def response_model_model1_annotation_model2_return_same_model() -> Item:
    return User(name="John", surname="Doe")


@app.get(
    "/response_model_model1-annotation_model2-return_exact_dict", response_model=User
)
def response_model_model1_annotation_model2_return_exact_dict() -> Item:
    return {"name": "John", "surname": "Doe"}


@app.get(
    "/response_model_model1-annotation_model2-return_invalid_dict", response_model=User
)
def response_model_model1_annotation_model2_return_invalid_dict() -> Item:
    return {"name": "John"}


@app.get(
    "/response_model_model1-annotation_model2-return_invalid_model", response_model=User
)
def response_model_model1_annotation_model2_return_invalid_model() -> Item:
    return Item(name="Foo", price=42.0)


@app.get(
    "/response_model_model1-annotation_model2-return_dict_with_extra_data",
    response_model=User,
)
def response_model_model1_annotation_model2_return_dict_with_extra_data() -> Item:
    return {"name": "John", "surname": "Doe", "password_hash": "secret"}


@app.get(
    "/response_model_model1-annotation_model2-return_submodel_with_extra_data",
    response_model=User,
)
def response_model_model1_annotation_model2_return_submodel_with_extra_data() -> Item:
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get(
    "/response_model_filtering_model-annotation_submodel-return_submodel",
    response_model=User,
)
def response_model_filtering_model_annotation_submodel_return_submodel() -> DBUser:
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get("/response_model_list_of_model-no_annotation", response_model=List[User])
def response_model_list_of_model_no_annotation():
    return [
        DBUser(name="John", surname="Doe", password_hash="secret"),
        DBUser(name="Jane", surname="Does", password_hash="secret2"),
    ]


@app.get("/no_response_model-annotation_list_of_model")
def no_response_model_annotation_list_of_model() -> List[User]:
    return [
        DBUser(name="John", surname="Doe", password_hash="secret"),
        DBUser(name="Jane", surname="Does", password_hash="secret2"),
    ]


@app.get("/no_response_model-annotation_forward_ref_list_of_model")
def no_response_model_annotation_forward_ref_list_of_model() -> "List[User]":
    return [
        DBUser(name="John", surname="Doe", password_hash="secret"),
        DBUser(name="Jane", surname="Does", password_hash="secret2"),
    ]


@app.get(
    "/response_model_union-no_annotation-return_model1",
    response_model=Union[User, Item],
)
def response_model_union_no_annotation_return_model1():
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get(
    "/response_model_union-no_annotation-return_model2",
    response_model=Union[User, Item],
)
def response_model_union_no_annotation_return_model2():
    return Item(name="Foo", price=42.0)


@app.get("/no_response_model-annotation_union-return_model1")
def no_response_model_annotation_union_return_model1() -> Union[User, Item]:
    return DBUser(name="John", surname="Doe", password_hash="secret")


@app.get("/no_response_model-annotation_union-return_model2")
def no_response_model_annotation_union_return_model2() -> Union[User, Item]:
    return Item(name="Foo", price=42.0)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/no_response_model-no_annotation-return_model": {
            "get": {
                "summary": "No Response Model No Annotation Return Model",
                "operationId": "no_response_model_no_annotation_return_model_no_response_model_no_annotation_return_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/no_response_model-no_annotation-return_dict": {
            "get": {
                "summary": "No Response Model No Annotation Return Dict",
                "operationId": "no_response_model_no_annotation_return_dict_no_response_model_no_annotation_return_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model-no_annotation-return_same_model": {
            "get": {
                "summary": "Response Model No Annotation Return Same Model",
                "operationId": "response_model_no_annotation_return_same_model_response_model_no_annotation_return_same_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model-no_annotation-return_exact_dict": {
            "get": {
                "summary": "Response Model No Annotation Return Exact Dict",
                "operationId": "response_model_no_annotation_return_exact_dict_response_model_no_annotation_return_exact_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model-no_annotation-return_invalid_dict": {
            "get": {
                "summary": "Response Model No Annotation Return Invalid Dict",
                "operationId": "response_model_no_annotation_return_invalid_dict_response_model_no_annotation_return_invalid_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model-no_annotation-return_invalid_model": {
            "get": {
                "summary": "Response Model No Annotation Return Invalid Model",
                "operationId": "response_model_no_annotation_return_invalid_model_response_model_no_annotation_return_invalid_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model-no_annotation-return_dict_with_extra_data": {
            "get": {
                "summary": "Response Model No Annotation Return Dict With Extra Data",
                "operationId": "response_model_no_annotation_return_dict_with_extra_data_response_model_no_annotation_return_dict_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model-no_annotation-return_submodel_with_extra_data": {
            "get": {
                "summary": "Response Model No Annotation Return Submodel With Extra Data",
                "operationId": "response_model_no_annotation_return_submodel_with_extra_data_response_model_no_annotation_return_submodel_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation-return_same_model": {
            "get": {
                "summary": "No Response Model Annotation Return Same Model",
                "operationId": "no_response_model_annotation_return_same_model_no_response_model_annotation_return_same_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation-return_exact_dict": {
            "get": {
                "summary": "No Response Model Annotation Return Exact Dict",
                "operationId": "no_response_model_annotation_return_exact_dict_no_response_model_annotation_return_exact_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation-return_invalid_dict": {
            "get": {
                "summary": "No Response Model Annotation Return Invalid Dict",
                "operationId": "no_response_model_annotation_return_invalid_dict_no_response_model_annotation_return_invalid_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation-return_invalid_model": {
            "get": {
                "summary": "No Response Model Annotation Return Invalid Model",
                "operationId": "no_response_model_annotation_return_invalid_model_no_response_model_annotation_return_invalid_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation-return_dict_with_extra_data": {
            "get": {
                "summary": "No Response Model Annotation Return Dict With Extra Data",
                "operationId": "no_response_model_annotation_return_dict_with_extra_data_no_response_model_annotation_return_dict_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation-return_submodel_with_extra_data": {
            "get": {
                "summary": "No Response Model Annotation Return Submodel With Extra Data",
                "operationId": "no_response_model_annotation_return_submodel_with_extra_data_no_response_model_annotation_return_submodel_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_none-annotation-return_same_model": {
            "get": {
                "summary": "Response Model None Annotation Return Same Model",
                "operationId": "response_model_none_annotation_return_same_model_response_model_none_annotation_return_same_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_none-annotation-return_exact_dict": {
            "get": {
                "summary": "Response Model None Annotation Return Exact Dict",
                "operationId": "response_model_none_annotation_return_exact_dict_response_model_none_annotation_return_exact_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_none-annotation-return_invalid_dict": {
            "get": {
                "summary": "Response Model None Annotation Return Invalid Dict",
                "operationId": "response_model_none_annotation_return_invalid_dict_response_model_none_annotation_return_invalid_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_none-annotation-return_invalid_model": {
            "get": {
                "summary": "Response Model None Annotation Return Invalid Model",
                "operationId": "response_model_none_annotation_return_invalid_model_response_model_none_annotation_return_invalid_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_none-annotation-return_dict_with_extra_data": {
            "get": {
                "summary": "Response Model None Annotation Return Dict With Extra Data",
                "operationId": "response_model_none_annotation_return_dict_with_extra_data_response_model_none_annotation_return_dict_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_none-annotation-return_submodel_with_extra_data": {
            "get": {
                "summary": "Response Model None Annotation Return Submodel With Extra Data",
                "operationId": "response_model_none_annotation_return_submodel_with_extra_data_response_model_none_annotation_return_submodel_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/response_model_model1-annotation_model2-return_same_model": {
            "get": {
                "summary": "Response Model Model1 Annotation Model2 Return Same Model",
                "operationId": "response_model_model1_annotation_model2_return_same_model_response_model_model1_annotation_model2_return_same_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_model1-annotation_model2-return_exact_dict": {
            "get": {
                "summary": "Response Model Model1 Annotation Model2 Return Exact Dict",
                "operationId": "response_model_model1_annotation_model2_return_exact_dict_response_model_model1_annotation_model2_return_exact_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_model1-annotation_model2-return_invalid_dict": {
            "get": {
                "summary": "Response Model Model1 Annotation Model2 Return Invalid Dict",
                "operationId": "response_model_model1_annotation_model2_return_invalid_dict_response_model_model1_annotation_model2_return_invalid_dict_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_model1-annotation_model2-return_invalid_model": {
            "get": {
                "summary": "Response Model Model1 Annotation Model2 Return Invalid Model",
                "operationId": "response_model_model1_annotation_model2_return_invalid_model_response_model_model1_annotation_model2_return_invalid_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_model1-annotation_model2-return_dict_with_extra_data": {
            "get": {
                "summary": "Response Model Model1 Annotation Model2 Return Dict With Extra Data",
                "operationId": "response_model_model1_annotation_model2_return_dict_with_extra_data_response_model_model1_annotation_model2_return_dict_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_model1-annotation_model2-return_submodel_with_extra_data": {
            "get": {
                "summary": "Response Model Model1 Annotation Model2 Return Submodel With Extra Data",
                "operationId": "response_model_model1_annotation_model2_return_submodel_with_extra_data_response_model_model1_annotation_model2_return_submodel_with_extra_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_filtering_model-annotation_submodel-return_submodel": {
            "get": {
                "summary": "Response Model Filtering Model Annotation Submodel Return Submodel",
                "operationId": "response_model_filtering_model_annotation_submodel_return_submodel_response_model_filtering_model_annotation_submodel_return_submodel_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                    }
                },
            }
        },
        "/response_model_list_of_model-no_annotation": {
            "get": {
                "summary": "Response Model List Of Model No Annotation",
                "operationId": "response_model_list_of_model_no_annotation_response_model_list_of_model_no_annotation_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Response Model List Of Model No Annotation Response Model List Of Model No Annotation Get",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation_list_of_model": {
            "get": {
                "summary": "No Response Model Annotation List Of Model",
                "operationId": "no_response_model_annotation_list_of_model_no_response_model_annotation_list_of_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response No Response Model Annotation List Of Model No Response Model Annotation List Of Model Get",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation_forward_ref_list_of_model": {
            "get": {
                "summary": "No Response Model Annotation Forward Ref List Of Model",
                "operationId": "no_response_model_annotation_forward_ref_list_of_model_no_response_model_annotation_forward_ref_list_of_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response No Response Model Annotation Forward Ref List Of Model No Response Model Annotation Forward Ref List Of Model Get",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/response_model_union-no_annotation-return_model1": {
            "get": {
                "summary": "Response Model Union No Annotation Return Model1",
                "operationId": "response_model_union_no_annotation_return_model1_response_model_union_no_annotation_return_model1_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Response Model Union No Annotation Return Model1 Response Model Union No Annotation Return Model1 Get",
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/User"},
                                        {"$ref": "#/components/schemas/Item"},
                                    ],
                                }
                            }
                        },
                    }
                },
            }
        },
        "/response_model_union-no_annotation-return_model2": {
            "get": {
                "summary": "Response Model Union No Annotation Return Model2",
                "operationId": "response_model_union_no_annotation_return_model2_response_model_union_no_annotation_return_model2_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Response Model Union No Annotation Return Model2 Response Model Union No Annotation Return Model2 Get",
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/User"},
                                        {"$ref": "#/components/schemas/Item"},
                                    ],
                                }
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation_union-return_model1": {
            "get": {
                "summary": "No Response Model Annotation Union Return Model1",
                "operationId": "no_response_model_annotation_union_return_model1_no_response_model_annotation_union_return_model1_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response No Response Model Annotation Union Return Model1 No Response Model Annotation Union Return Model1 Get",
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/User"},
                                        {"$ref": "#/components/schemas/Item"},
                                    ],
                                }
                            }
                        },
                    }
                },
            }
        },
        "/no_response_model-annotation_union-return_model2": {
            "get": {
                "summary": "No Response Model Annotation Union Return Model2",
                "operationId": "no_response_model_annotation_union_return_model2_no_response_model_annotation_union_return_model2_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response No Response Model Annotation Union Return Model2 No Response Model Annotation Union Return Model2 Get",
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/User"},
                                        {"$ref": "#/components/schemas/Item"},
                                    ],
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
            "Item": {
                "title": "Item",
                "required": ["name", "price"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {"title": "Price", "type": "number"},
                },
            },
            "User": {
                "title": "User",
                "required": ["name", "surname"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "surname": {"title": "Surname", "type": "string"},
                },
            },
        }
    },
}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_no_response_model_no_annotation_return_model():
    response = client.get("/no_response_model-no_annotation-return_model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_no_response_model_no_annotation_return_dict():
    response = client.get("/no_response_model-no_annotation-return_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_no_annotation_return_same_model():
    response = client.get("/response_model-no_annotation-return_same_model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_no_annotation_return_exact_dict():
    response = client.get("/response_model-no_annotation-return_exact_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_no_annotation_return_invalid_dict():
    with pytest.raises(ValidationError):
        client.get("/response_model-no_annotation-return_invalid_dict")


def test_response_model_no_annotation_return_invalid_model():
    with pytest.raises(ValidationError):
        client.get("/response_model-no_annotation-return_invalid_model")


def test_response_model_no_annotation_return_dict_with_extra_data():
    response = client.get("/response_model-no_annotation-return_dict_with_extra_data")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_no_annotation_return_submodel_with_extra_data():
    response = client.get(
        "/response_model-no_annotation-return_submodel_with_extra_data"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_no_response_model_annotation_return_same_model():
    response = client.get("/no_response_model-annotation-return_same_model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_no_response_model_annotation_return_exact_dict():
    response = client.get("/no_response_model-annotation-return_exact_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_no_response_model_annotation_return_invalid_dict():
    with pytest.raises(ValidationError):
        client.get("/no_response_model-annotation-return_invalid_dict")


def test_no_response_model_annotation_return_invalid_model():
    with pytest.raises(ValidationError):
        client.get("/no_response_model-annotation-return_invalid_model")


def test_no_response_model_annotation_return_dict_with_extra_data():
    response = client.get("/no_response_model-annotation-return_dict_with_extra_data")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_no_response_model_annotation_return_submodel_with_extra_data():
    response = client.get(
        "/no_response_model-annotation-return_submodel_with_extra_data"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_none_annotation_return_same_model():
    response = client.get("/response_model_none-annotation-return_same_model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_none_annotation_return_exact_dict():
    response = client.get("/response_model_none-annotation-return_exact_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_none_annotation_return_invalid_dict():
    response = client.get("/response_model_none-annotation-return_invalid_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John"}


def test_response_model_none_annotation_return_invalid_model():
    response = client.get("/response_model_none-annotation-return_invalid_model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo", "price": 42.0}


def test_response_model_none_annotation_return_dict_with_extra_data():
    response = client.get("/response_model_none-annotation-return_dict_with_extra_data")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "John",
        "surname": "Doe",
        "password_hash": "secret",
    }


def test_response_model_none_annotation_return_submodel_with_extra_data():
    response = client.get(
        "/response_model_none-annotation-return_submodel_with_extra_data"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "John",
        "surname": "Doe",
        "password_hash": "secret",
    }


def test_response_model_model1_annotation_model2_return_same_model():
    response = client.get("/response_model_model1-annotation_model2-return_same_model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_model1_annotation_model2_return_exact_dict():
    response = client.get("/response_model_model1-annotation_model2-return_exact_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_model1_annotation_model2_return_invalid_dict():
    with pytest.raises(ValidationError):
        client.get("/response_model_model1-annotation_model2-return_invalid_dict")


def test_response_model_model1_annotation_model2_return_invalid_model():
    with pytest.raises(ValidationError):
        client.get("/response_model_model1-annotation_model2-return_invalid_model")


def test_response_model_model1_annotation_model2_return_dict_with_extra_data():
    response = client.get(
        "/response_model_model1-annotation_model2-return_dict_with_extra_data"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_model1_annotation_model2_return_submodel_with_extra_data():
    response = client.get(
        "/response_model_model1-annotation_model2-return_submodel_with_extra_data"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_filtering_model_annotation_submodel_return_submodel():
    response = client.get(
        "/response_model_filtering_model-annotation_submodel-return_submodel"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_list_of_model_no_annotation():
    response = client.get("/response_model_list_of_model-no_annotation")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "John", "surname": "Doe"},
        {"name": "Jane", "surname": "Does"},
    ]


def test_no_response_model_annotation_list_of_model():
    response = client.get("/no_response_model-annotation_list_of_model")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "John", "surname": "Doe"},
        {"name": "Jane", "surname": "Does"},
    ]


def test_no_response_model_annotation_forward_ref_list_of_model():
    response = client.get("/no_response_model-annotation_forward_ref_list_of_model")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "John", "surname": "Doe"},
        {"name": "Jane", "surname": "Does"},
    ]


def test_response_model_union_no_annotation_return_model1():
    response = client.get("/response_model_union-no_annotation-return_model1")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_response_model_union_no_annotation_return_model2():
    response = client.get("/response_model_union-no_annotation-return_model2")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo", "price": 42.0}


def test_no_response_model_annotation_union_return_model1():
    response = client.get("/no_response_model-annotation_union-return_model1")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "John", "surname": "Doe"}


def test_no_response_model_annotation_union_return_model2():
    response = client.get("/no_response_model-annotation_union-return_model2")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo", "price": 42.0}
