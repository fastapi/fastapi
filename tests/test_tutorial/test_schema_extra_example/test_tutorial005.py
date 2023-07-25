from dirty_equals import IsPartialDict
from fastapi.testclient import TestClient

from docs_src.schema_extra_example.tutorial005 import app

client = TestClient(app)


# Test required and embedded body parameters with no bodies sent
def test_post_body_example():
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    )
    assert response.status_code == 200


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    openapi = response.json()
    assert openapi == IsPartialDict(
        paths={
            "/items/{item_id}": {
                "put": IsPartialDict(
                    parameters=[
                        IsPartialDict(
                            schema=IsPartialDict(examples=[5, "5", "anything else"]),
                            examples={
                                "id as int": {"value": 5},
                                "id as string": {"value": "5"},
                                "invalid id": {"value": "anything else"},
                            },
                        )
                    ],
                    requestBody=IsPartialDict(
                        content=IsPartialDict(
                            **{
                                "application/json": IsPartialDict(
                                    schema=IsPartialDict(
                                        examples=[
                                            {
                                                "name": "Foo",
                                                "description": "A very nice Item",
                                                "price": 35.4,
                                                "tax": 3.2,
                                            },
                                            {
                                                "name": "Bar",
                                                "price": "35.4",
                                            },
                                            {
                                                "name": "Baz",
                                                "price": "thirty five point four",
                                            },
                                        ]
                                    ),
                                    examples={
                                        "Example Item": {
                                            "value": {
                                                "name": "Foo",
                                                "description": "A very nice Item",
                                                "price": 35.4,
                                                "tax": 3.2,
                                            }
                                        },
                                        "Example Item; coerce string to float": {
                                            "value": {
                                                "name": "Bar",
                                                "price": "35.4",
                                            }
                                        },
                                        "Raise validation error for 'price'": {
                                            "value": {
                                                "name": "Baz",
                                                "price": "thirty five point four",
                                            }
                                        },
                                    },
                                )
                            }
                        )
                    ),
                )
            }
        }
    )
