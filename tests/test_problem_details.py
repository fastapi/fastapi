import http.client

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ProblemDetailsResponse
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


def test_problem_details_response_content_type():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Item not found")

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"


def test_http_exception_string_detail():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Item not found")

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 404
    data = response.json()
    assert data["type"] == "about:blank"
    assert data["title"] == "Not Found"
    assert data["status"] == 404
    assert data["detail"] == "Item not found"
    assert "instance" in data
    assert "errors" not in data


def test_http_exception_dict_detail():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(
            status_code=422,
            detail={"code": "CUSTOM_ERROR", "message": "Something went wrong"},
        )

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 422
    data = response.json()
    assert data["title"] == http.client.responses.get(422)
    assert data["status"] == 422
    assert "detail" not in data
    assert "errors" in data
    assert data["errors"] == {"code": "CUSTOM_ERROR", "message": "Something went wrong"}


def test_http_exception_list_detail():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=400, detail=["err1", "err2"])

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 400
    data = response.json()
    assert "detail" not in data
    assert data["errors"] == ["err1", "err2"]


def test_http_exception_with_headers():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(
            status_code=404,
            detail="Not found",
            headers={"X-Error": "custom"},
        )

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 404
    assert response.headers.get("x-error") == "custom"
    assert response.json()["detail"] == "Not found"


def test_no_body_status_code_204():
    app = FastAPI(problem_details=True)

    @app.get("/no-body")
    def no_body():
        raise HTTPException(status_code=204)

    client = TestClient(app)
    response = client.get("/no-body")
    assert response.status_code == 204
    assert not response.content


def test_no_body_status_code_304():
    app = FastAPI(problem_details=True)

    @app.get("/no-body")
    def no_body():
        raise HTTPException(status_code=304)

    client = TestClient(app)
    response = client.get("/no-body")
    assert response.status_code == 304
    assert not response.content


def test_no_body_status_code_with_detail():
    app = FastAPI(problem_details=True)

    @app.get("/no-body")
    def no_body():
        raise HTTPException(status_code=204, detail="should disappear")

    client = TestClient(app)
    response = client.get("/no-body")
    assert response.status_code == 204
    assert not response.content


def test_validation_error():
    app = FastAPI(problem_details=True)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.get("/items/foo")
    assert response.status_code == 422
    data = response.json()
    assert data["type"] == "validation-error"
    assert data["title"] == "Validation Error"
    assert data["status"] == 422
    assert data["detail"] == "1 validation error"
    assert "instance" in data
    assert "errors" in data
    assert len(data["errors"]) == 1
    assert data["errors"][0]["loc"] == ["path", "item_id"]
    assert data["errors"][0]["type"] == "int_parsing"


def test_multiple_validation_errors():
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        price: float

    app = FastAPI(problem_details=True)

    @app.post("/items")
    def create_item(item: Item):
        return item

    client = TestClient(app)
    response = client.post("/items", json={})
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "2 validation errors"
    assert len(data["errors"]) == 2


def test_validation_error_content_type():
    app = FastAPI(problem_details=True)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.get("/items/foo")
    assert response.headers["content-type"] == "application/problem+json"


def test_validation_error_overridden_by_custom_handler():
    app = FastAPI(problem_details=True)

    @app.exception_handler(RequestValidationError)
    async def custom_handler(request, exc):
        from starlette.responses import JSONResponse

        return JSONResponse({"custom": "handler"}, status_code=422)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.get("/items/foo")
    assert response.json() == {"custom": "handler"}


def test_http_exception_overridden_by_custom_handler():
    app = FastAPI(problem_details=True)

    @app.exception_handler(HTTPException)
    async def custom_handler(request, exc):
        from starlette.responses import JSONResponse

        return JSONResponse({"custom": "http"}, status_code=exc.status_code)

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404)

    client = TestClient(app)
    response = client.get("/error")
    assert response.json() == {"custom": "http"}


def test_default_false_uses_legacy_format():
    app = FastAPI(problem_details=False)

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Not found")

    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Not found"}


def test_default_false_validation_uses_legacy_format():
    app = FastAPI(problem_details=False)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.get("/items/foo")
    assert response.status_code == 422
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)


def test_problem_details_not_inherited_by_default():
    app = FastAPI()

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Not found")

    client = TestClient(app)
    response = client.get("/error")
    assert response.headers["content-type"] == "application/json"


def test_openapi_schema_with_problem_details():
    app = FastAPI(problem_details=True)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    assert schema["paths"]["/items/{item_id}"]["get"]["responses"]["422"] == snapshot(
        {
            "description": "Validation Error",
            "content": {
                "application/problem+json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetails"}
                }
            },
        }
    )
    assert "ProblemDetails" in schema["components"]["schemas"]
    assert (
        schema["components"]["schemas"]["ProblemDetails"]["title"] == "ProblemDetails"
    )


def test_openapi_schema_without_problem_details():
    app = FastAPI(problem_details=False)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    assert (
        schema["paths"]["/items/{item_id}"]["get"]["responses"]["422"]["content"][
            "application/json"
        ]["schema"]["$ref"]
        == "#/components/schemas/HTTPValidationError"
    )
    assert "HTTPValidationError" in schema["components"]["schemas"]


def test_openapi_schema_default():
    app = FastAPI()

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    assert "HTTPValidationError" in schema["components"]["schemas"]
    assert "ProblemDetails" not in schema["components"]["schemas"]


def test_problem_details_response_class():
    response = ProblemDetailsResponse(
        content={"type": "about:blank", "title": "Error", "status": 400},
        status_code=400,
    )
    assert response.media_type == "application/problem+json"
    assert response.status_code == 400


def test_problem_details_handler_request_without_app():
    from fastapi.exception_handlers import _get_problem_details_config
    from starlette.requests import Request

    request = Request(
        scope={"type": "http", "method": "GET", "path": "/", "headers": []}
    )
    result = _get_problem_details_config(request)
    assert result == (None, None)


def test_unicode_status_code():
    app = FastAPI(problem_details=True)

    @app.get("/teapot")
    def teapot():
        raise HTTPException(status_code=418)

    client = TestClient(app)
    response = client.get("/teapot")
    assert response.status_code == 418
    data = response.json()
    assert data["title"] == "I'm a Teapot"
    assert data["status"] == 418


def test_instance_url_reflects_request():
    app = FastAPI(problem_details=True)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app, base_url="http://testserver")
    response = client.get("/items/abc")
    data = response.json()
    assert data["instance"] == "http://testserver/items/abc"


def test_explicit_type_on_http_exception():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(
            status_code=404, detail="Not found", type="my-custom-problem"
        )

    client = TestClient(app)
    response = client.get("/error")
    data = response.json()
    assert data["type"] == "my-custom-problem"


def test_explicit_absolute_type_uri():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(
            status_code=404,
            detail="Not found",
            type="https://example.com/errors/custom",
        )

    client = TestClient(app)
    response = client.get("/error")
    data = response.json()
    assert data["type"] == "https://example.com/errors/custom"


def test_type_base_uri_auto_derivation():
    app = FastAPI(
        problem_details=True,
        problem_type_base_uri="https://example.com/errors",
    )

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Not found")

    client = TestClient(app)
    response = client.get("/error")
    data = response.json()
    assert data["type"] == "https://example.com/errors/not-found"


def test_type_base_uri_with_problem_types_map():
    app = FastAPI(
        problem_details=True,
        problem_type_base_uri="https://example.com/errors",
        problem_types={404: "order-not-found"},
    )

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Not found")

    client = TestClient(app)
    response = client.get("/error")
    data = response.json()
    assert data["type"] == "https://example.com/errors/order-not-found"


def test_explicit_type_overrides_problem_types_map():
    app = FastAPI(
        problem_details=True,
        problem_type_base_uri="https://example.com/errors",
        problem_types={404: "order-not-found"},
    )

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Not found", type="custom-override")

    client = TestClient(app)
    response = client.get("/error")
    data = response.json()
    assert data["type"] == "https://example.com/errors/custom-override"


def test_validation_error_type_with_base_uri():
    app = FastAPI(
        problem_details=True,
        problem_type_base_uri="https://example.com/errors",
    )

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.get("/items/foo")
    data = response.json()
    assert data["type"] == "https://example.com/errors/validation-error"


def test_validation_error_problem_types_map():
    app = FastAPI(
        problem_details=True,
        problem_type_base_uri="https://example.com/errors",
        problem_types={422: "bad-input"},
    )

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.get("/items/foo")
    data = response.json()
    assert data["type"] == "https://example.com/errors/bad-input"


def test_no_base_uri_falls_back_to_segment():
    app = FastAPI(problem_details=True)

    @app.get("/error")
    def raise_error():
        raise HTTPException(status_code=404, detail="Not found")

    client = TestClient(app)
    response = client.get("/error")
    data = response.json()
    assert data["type"] == "about:blank"


def test_openapi_schema_problem_details_has_additional_properties():
    app = FastAPI(problem_details=True)

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    pd_schema = schema["components"]["schemas"]["ProblemDetails"]
    assert pd_schema.get("additionalProperties") is True
