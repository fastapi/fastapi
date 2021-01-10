import pytest
from fastapi import FastAPI
from fastapi.routing import ViewAPIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

router = ViewAPIRouter()
app = FastAPI()


class Item(BaseModel):
    message_update: str


@router.view()
class Messages(ViewAPIRouter.View):
    def __init__(self, message: str):
        self.message = message

    @router.get("/message")
    def get_message(self) -> str:
        return self.message

    @router.post("/message")
    def post_message(self, item: Item) -> str:
        self.message = item.message_update


instance = Messages(message="👋")
app.include_router(router)
client = TestClient(app)


def test_view_api_router():

    # verify route inclusion
    response = client.get("/message")
    assert response.status_code == 200, response.text
    assert instance.message in response.text

    # change state in the instance
    item = Item(message_update="✨")
    response = client.post("/message", json=item.dict())
    assert response.status_code == 200, response.text

    # verify the same instance is provided to both methods
    response = client.get("/message")
    assert response.status_code == 200, response.text
    assert item.message_update in response.text


def test_view_api_router_exceptions():
    router = ViewAPIRouter()

    @router.view()
    class First(ViewAPIRouter.View):
        pass

    with pytest.raises(Exception) as exception:

        @router.view()
        class Second(ViewAPIRouter.View):
            pass

    assert "must be applied to exactly one" in str(exception)

    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:

        @router.view()
        def not_a_class():
            pass  # pragma: no cover

    assert "must be applied to a class" in str(exception)

    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:

        @router.view()
        class Third(ViewAPIRouter):
            pass

    assert "must be applied to a subclass of" in str(exception)

    app = FastAPI()
    router = ViewAPIRouter()
    with pytest.raises(Exception) as exception:
        app.include_router(router)

    assert "was not be bound to a view instance" in str(exception)
