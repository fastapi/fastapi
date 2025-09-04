from fastapi.testclient import TestClient

from docs_src.metadata.tutorial001_1 import app

client = TestClient(app)


def test_items():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"name": "Katana"}]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {
            "title": "ChimichangApp",
            "summary": "Deadpool's favorite app. Nuff said.",
            "description": "\nChimichangApp API helps you do awesome stuff. 🚀\n\n## Items\n\nYou can **read items**.\n\n## Users\n\nYou will be able to:\n\n* **Create users** (_not implemented_).\n* **Read users** (_not implemented_).\n",
            "termsOfService": "http://example.com/terms/",
            "contact": {
                "name": "Deadpoolio the Amazing",
                "url": "http://x-force.example.com/contact/",
                "email": "dp@x-force.example.com",
            },
            "license": {
                "name": "Apache 2.0",
                "identifier": "MIT",
            },
            "version": "0.0.1",
        },
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            }
        },
    }
