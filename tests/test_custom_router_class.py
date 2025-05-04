from fastapi import APIRouter, FastAPI, status
from fastapi.testclient import TestClient
from starlette.datastructures import MutableHeaders


class CustomAPIRouter(APIRouter):
    async def __call__(self, scope, receive, send):
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["x-custom-header"] = "custom-value"

            await send(message)

        await super().__call__(scope, receive, send_wrapper)


app = FastAPI(
    router_class=CustomAPIRouter,
)


@app.get("/")
def get_root():
    return {"message": "root"}


client = TestClient(app)


def test_get():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "root"}
    assert response.headers["x-custom-header"] == "custom-value"


def test_route_classes():
    assert isinstance(app.router, CustomAPIRouter)
