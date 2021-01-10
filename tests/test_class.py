from fastapi import FastAPI
from fastapi.routing import LateBoundAPIRouter
from fastapi.testclient import TestClient

router = LateBoundAPIRouter(instance_delegate=lambda: EncapsulatedRoutes.INSTANCE)
app = FastAPI()


class EncapsulatedRoutes:
    INSTANCE = None

    def __init__(self):
        EncapsulatedRoutes.INSTANCE = self

    @router.get("/get_message")
    def get_message(self) -> str:
        return "👋"


app.include_router(router, is_late_bound=True)
client = TestClient(app)


def test_late_bound_router():
    response = client.get("/get_message")
    assert response.status_code == 200, response.text
    assert "👋" in response.text
