import pytest
from fastapi import FastAPI
from fastapi.routing import ViewAPIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

view_router = ViewAPIRouter()
app = FastAPI()


class Item(BaseModel):
    message_update: str


@view_router.bind_to_class()
class Messages(ViewAPIRouter.View):
    def __init__(self, message: str):
        self.message = message

    @view_router.get("/message")
    def get_message(self) -> str:
        return self.message

    @view_router.post("/message")
    def post_message(self, item: Item) -> str:
        self.message = item.message_update


em_instance = Messages(message="👋")
pt_instance = Messages(message="olá")
en_instance = Messages(message="hello")
app.include_router(em_instance.router, prefix="/em")
app.include_router(pt_instance.router, prefix="/pt")
app.include_router(en_instance.router, prefix="/en")
client = TestClient(app)


def test_view_api_router():

    # verify route inclusion
    response = client.get("/em/message")
    assert response.status_code == 200, response.text
    assert em_instance.message in response.text
    response = client.get("/pt/message")
    assert response.status_code == 200, response.text
    assert pt_instance.message in response.text
    response = client.get("/en/message")
    assert response.status_code == 200, response.text
    assert en_instance.message in response.text

    # change state in an instance
    item = Item(message_update="✨")
    response = client.post("/em/message", json=item.dict())
    assert response.status_code == 200, response.text
    response = client.get("/em/message")
    assert response.status_code == 200, response.text
    assert item.message_update in response.text


def test_view_api_router_exceptions():
    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:
        router.bind_to_class()("not a class")

    assert "decorator must be applied to a class" in str(exception)

    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:
        router.bind_to_class()(Exception)
        router.bind_to_class()(Exception)

    assert "decorator can only be applied once" in str(exception)

    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:
        router.get("/path")("endpoint")

    assert "cannot be applied before binding to a class" in str(exception)

    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:
        router.bind_to_class()(Exception)
        router.get("/path")("endpoint")

    assert "cannot be applied outside its bound class" in str(exception)

    app = FastAPI()
    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:
        app.include_router(router)

    assert "must be bound to a class" in str(exception)
