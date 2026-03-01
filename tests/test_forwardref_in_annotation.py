from typing import Annotated, ForwardRef

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


def test_annotated_forwardref_dependency():
    app = FastAPI()

    User = ForwardRef("User")

    def get_user() -> "User":
        return {"name": "amulya"}

    @app.get("/")
    def read_user(user: Annotated[User, Depends(get_user)]):
        return user

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"name": "amulya"}
