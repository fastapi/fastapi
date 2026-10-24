from typing import Annotated

import pytest
from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import Field, create_model


def parameter_endpoint(model, parameter):
    def read(values):
        return values

    read.__annotations__ = {"values": Annotated[model, parameter()]}
    return read


@pytest.mark.parametrize("model_count", [128, 129, 160])
@pytest.mark.parametrize(
    "parameter,location", [(Query, "query"), (Header, "header"), (Cookie, "cookie")]
)
def test_openapi_parameter_models_survive_cache_capacity(
    model_count, parameter, location
):
    app = FastAPI()
    for index in range(model_count):
        model = create_model(
            f"Parameters{index}",
            value=(int, Field(default=1, ge=1, le=10)),
        )
        app.add_api_route(f"/items/{index}", parameter_endpoint(model, parameter))

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert len(schema["paths"]) == model_count
    for index in range(model_count):
        value = schema["paths"][f"/items/{index}"]["get"]["parameters"][0]
        assert value["name"] == "value"
        assert value["in"] == location
        assert value["required"] is False
        assert value["schema"]["default"] == 1
        assert value["schema"]["minimum"] == 1
        assert value["schema"]["maximum"] == 10

    for index in [0, model_count - 1]:
        response = client.get(f"/items/{index}")
        assert response.status_code == 200, response.text
        assert response.json() == {"value": 1}
        for supplied, status in [(2, 200), (0, 422)]:
            options = {}
            if location == "cookie":
                client.cookies.set("value", str(supplied))
            else:
                options["params" if location == "query" else "headers"] = {
                    "value": str(supplied)
                }
            response = client.get(f"/items/{index}", **options)
            assert response.status_code == status, response.text
            if status == 200:
                assert response.json() == {"value": supplied}
            else:
                assert response.json()["detail"][0]["loc"] == [location, "value"]
        client.cookies.clear()
