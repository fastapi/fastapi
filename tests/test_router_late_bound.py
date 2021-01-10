from fastapi import FastAPI
from fastapi.routing import LateBoundAPIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

router = LateBoundAPIRouter(instance_delegate=lambda: EncapsulatedRoutes.INSTANCE)
app = FastAPI()


class Item(BaseModel):
    message_update: str


class EncapsulatedRoutes:
    INSTANCE = None

    def __init__(self, message: str):
        EncapsulatedRoutes.INSTANCE = self
        self.message = message

    @router.get("/message")
    def get_message(self) -> str:
        return self.message

    @router.post("/message")
    def post_message(self, item: Item) -> str:
        self.message = item.message_update


app.include_router(router, is_late_bound=True)
client = TestClient(app)
instance = EncapsulatedRoutes(message="👋")


def test_late_bound_router():
    response = client.get("/message")
    assert response.status_code == 200, response.text
    assert instance.message in response.text

    item = Item(message_update="✨")
    response = client.post("/message", json=item.dict())
    assert response.status_code == 200, response.text

    response = client.get("/message")
    assert response.status_code == 200, response.text
    assert item.message_update in response.text
