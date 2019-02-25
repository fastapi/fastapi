from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient

app = FastAPI()


tag1 = APIRouter(tags=["tag1"])
tag2 = APIRouter(tags=["tag2, tag1"])


@tag1.get("/")
async def tag1_root():
    return {"Tag": "tag1"}


@tag1.get("/test")
async def tag1_test():
    return {"Tag": "test"}


@tag2.get("/")
async def tag2_root():
    return {"Tag": "tag2 and tag1"}


@tag2.get("/test")
async def tag1_test():
    return {"Tag": "test"}


app.include_router(tag1, prefix="/tag1prefix")
app.include_router(tag2, prefix="/tag2prefix")


client = TestClient(app)


def test_tags_in_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json().get("paths").get("/tag1prefix/").get("get").get("tags") == [
        "tag1"
    ]
    assert response.json().get("paths").get("/tag1prefix/test").get("get").get(
        "tags"
    ) == ["tag1"]

    assert response.json().get("paths").get("/tag2prefix/").get("get").get("tags") == [
        "tag2, tag1"
    ]
    assert response.json().get("paths").get("/tag2prefix/test").get("get").get(
        "tags"
    ) == ["tag2, tag1"]
