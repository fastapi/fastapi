from fastapi import FastAPI, Request
from fastapi.route_middleware import log_route, route_middleware, verify_jwt
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/secure")
@route_middleware(verify_jwt, log_route)
async def secure_route(req: Request, is_true: bool):
    return {"status": "ok", "is_true": is_true, "user": req.user}


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
