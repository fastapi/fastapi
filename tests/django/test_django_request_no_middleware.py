import pytest
from fastapi import FastAPI
from fastapi.django import DjangoRequestDep
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def django_user(django_request: DjangoRequestDep):
    user = django_request.user

    if not user.is_authenticated:
        return {"error": "User not authenticated"}

    return {"username": user.username}


client = TestClient(app)


def test_returns_an_error():
    with pytest.raises(ValueError, match="Django Request not found"):
        client.get("/")
