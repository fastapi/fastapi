from fastapi import FastAPI, Form
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/")
def route_with_form(form_param: str = Form(alias="aliased-field")):
    return {}


client = TestClient(app)


def test_get_route():
    response = client.post("/", data={"aliased-field": "Hello, World!"})
    assert response.status_code == 200, response.text
    assert response.json() == {}


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    form_properties = (
        response.json()
        ["components"]["schemas"]["Body_route_with_form__post"]["properties"]
    )
    assert "aliased-field" in form_properties
