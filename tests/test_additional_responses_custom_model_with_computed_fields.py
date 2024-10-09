from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from pydantic.fields import computed_field


class Rectangle(BaseModel):
    width: int
    height: int

    @computed_field
    def area(self) -> int:
        return self.width * self.height


app = FastAPI()


@app.get(
    "/rectangle/",
    responses={
        200: {
            "model": Rectangle,
        },
    },
)
async def rectangle() -> Rectangle:
    return Rectangle(
        width=10,
        height=5,
    )


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/rectangle/": {
                "get": {
                    "summary": "Rectangle",
                    "operationId": "rectangle_rectangle__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Rectangle"}
                                }
                            },
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Rectangle": {
                    "properties": {
                        "width": {"type": "integer", "title": "Width"},
                        "height": {"type": "integer", "title": "Height"},
                        "area": {"type": "integer", "title": "Area", "readOnly": True},
                    },
                    "type": "object",
                    "required": ["width", "height", "area"],
                    "title": "Rectangle",
                }
            }
        },
    }
