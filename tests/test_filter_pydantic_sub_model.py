from fastapi import Depends, FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class ModelB(BaseModel):
    username: str


class ModelC(ModelB):
    password: str


class ModelA(BaseModel):
    name: str
    description: str = None
    model_b: ModelB


async def get_model_c() -> ModelC:
    return ModelC(username="test-user", password="test-password")


@app.get("/model", response_model=ModelA)
async def get_model_a(model_c=Depends(get_model_c)):
    return {"name": "model-a-name", "description": "model-a-desc", "model_b": model_c}


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/model": {
            "get": {
                "summary": "Get Model A",
                "operationId": "get_model_a_model_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ModelA"}
                            }
                        },
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "ModelA": {
                "title": "ModelA",
                "required": ["name", "model_b"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "description": {"title": "Description", "type": "string"},
                    "model_b": {"$ref": "#/components/schemas/ModelB"},
                },
            },
            "ModelB": {
                "title": "ModelB",
                "required": ["username"],
                "type": "object",
                "properties": {"username": {"title": "Username", "type": "string"}},
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_filter_sub_model():
    response = client.get("/model")
    assert response.status_code == 200
    assert response.json() == {
        "name": "model-a-name",
        "description": "model-a-desc",
        "model_b": {"username": "test-user"},
    }
