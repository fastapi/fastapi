from django.contrib.auth import aget_user
from fastapi import FastAPI
from fastapi.django import DjangoMiddleware, DjangoRequestDep
from fastapi.testclient import TestClient

app = FastAPI()
app.add_middleware(DjangoMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/current-user")
async def django_user(django_request: DjangoRequestDep):
    user = await aget_user(django_request)

    if not user.is_authenticated:
        return {"error": "User not authenticated"}

    return {"username": user.username}


client = TestClient(app)


def test_unauthenticated():
    response = client.get("/current-user")

    assert response.status_code == 200

    assert response.json() == {"error": "User not authenticated"}


def test_authenticated(authenticated_session_id: str):
    client.cookies.set("sessionid", authenticated_session_id)

    response = client.get("/current-user")

    assert response.status_code == 200

    assert response.json() == {"username": "test"}


def test_route_with_no_django_request():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {"message": "Hello World"}
