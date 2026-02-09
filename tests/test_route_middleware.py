import pytest
from fastapi import FastAPI, Request
from fastapi.route_middleware import route_middleware
from fastapi.testclient import TestClient


# Example middlewares for testing
async def verify_jwt(req: Request):
    if not (req.query_params.get("is_true") == "true"):
        req.scope["user"] = {"name": "xyz", "admin": True}
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid JWT")


def log_route(req: Request):
    print(f"[LOG] Path: {req.url.path}")


app = FastAPI()


@app.post("/secure")
@route_middleware(verify_jwt, log_route)
async def secure_route(req: Request, is_true: bool):
    return {"status": "ok", "is_true": is_true, "user": req.scope.get("user")}


@app.post("/open")
async def open_route(is_true: bool):
    return {"status": "open", "is_true": is_true}


client = TestClient(app)


def test_secure_route_pass():
    response = client.post("/secure?is_true=true")
    assert response.status_code == 200


def test_secure_route_fail():
    response = client.post("/secure?is_true=false")
    assert response.status_code == 403


def test_open_route():
    response = client.post("/open?is_true=false")
    assert response.status_code == 200


def test_route_middleware_wrong_param_name():
    # If the param name is not 'req', it should fail
    # We use a separate app to avoid polluting the main 'app'
    local_app = FastAPI()

    @local_app.get("/wrong-param")
    @route_middleware(log_route)
    async def wrong_param_handler(request: Request):
        return {"msg": "ok"}  # pragma: no cover

    with pytest.raises(
        ValueError, match="Route must have 'request: Request' parameter"
    ):
        TestClient(local_app).get("/wrong-param")
