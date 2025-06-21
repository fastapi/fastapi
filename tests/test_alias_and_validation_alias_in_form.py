"""
testing to fix incompatibility with alias and validation_alias between fastapi and PYDANTIC_V2
"""

from fastapi import FastAPI, Form
from fastapi._compat import PYDANTIC_V2
from starlette.testclient import TestClient

app: FastAPI = FastAPI()


@app.post("/testing_alias")
async def check_alias(id_test: int = Form(alias="otherId")):
    return {"other_id": id_test}


@app.post("/testing_validation_alias")
async def check_validation_alias(id_test: int = Form(validation_alias="otherId")):
    return {"other_id": id_test}


client = TestClient(app)


def test_get_alias():
    response = client.post("/testing_alias", data={"otherId": "1"})
    assert response.status_code == 200
    assert response.json() == {"other_id": 1}


def test_get_validation_alias():
    if PYDANTIC_V2:
        data = {"otherId": "1"}
    else:
        data = {"id_test": "1"}
    response = client.post("/testing_validation_alias", data=data)
    assert response.status_code == 200
    assert response.json() == {"other_id": 1}


def test_file_alias_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    if PYDANTIC_V2:
        schema = response.json()
        assert (
            "otherId"
            in schema["components"]["schemas"]["Body_check_alias_testing_alias_post"][
                "properties"
            ]
        )

        assert (
            "otherId"
            in schema["components"]["schemas"][
                "Body_check_validation_alias_testing_validation_alias_post"
            ]["properties"]
        )
