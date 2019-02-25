import pytest
from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient


@pytest.fixture()
def framework():
    app = FastAPI()
    tag1 = APIRouter(tags=["tag1"])
    tag2 = APIRouter(tags=["tag2", "tag1"])
    tag3 = APIRouter(tags=["tag2", "tag1"])

    @tag1.get("/get")
    async def tag1_get():
        return {"Tag": "tag1"}

    @tag1.put("/put")
    async def tag1_put():
        return {"Tag": "tag1"}

    @tag1.post("/post")
    async def tag1_post():
        return {"Tag": "tag1"}

    @tag1.delete("/delete")
    async def tag1_delete():
        return {"Tag": "tag1"}

    @tag1.options("/options")
    async def tag1_options():
        return {"Tag": "tag1"}

    @tag1.head("/head")
    async def tag1_head():
        return {"Tag": "tag1"}

    @tag1.patch("/patch")
    async def tag1_patch():
        return {"Tag": "tag1"}

    @tag1.trace("/trace")
    async def tag1_trace():
        return {"Tag": "tag1"}

    @tag2.get("/get")
    async def tag2_get():
        return {"Tag": "tag2"}

    @tag3.get("/get", tags=["tag3"])
    async def tag3_get():
        return {"Tag": "tag3"}

    app.include_router(tag1, prefix="/tag1prefix")
    app.include_router(tag2, prefix="/tag2prefix")
    app.include_router(tag3, prefix="/tag3prefix")

    yield app


data = [
    (
        "tag1",
        ["get", "put", "post", "delete", "options", "patch", "trace"],
        ["tag1"],
        {"Tag": "tag1"},
    ),
    ("tag2", ["get"], ["tag2", "tag1"], {"Tag": "tag2"}),
    ("tag3", ["get"], ["tag2", "tag1", "tag3"], {"Tag": "tag3"}),
]


@pytest.mark.parametrize("tag, methods, expected_tags, expected_json", data)
def test_tags_in_schema(framework, tag, methods, expected_tags, expected_json):
    with TestClient(framework) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        print(response.json())
        for method in methods:
            assert (
                response.json()
                .get("paths")
                .get(f"/{tag}prefix/{method}")
                .get(method)
                .get("tags")
                == expected_tags
            )
            url = framework.url_path_for(f"{tag}_{method}")
            rresponse = client.request(method, url)
            assert rresponse.status_code == 200
            assert rresponse.json() == expected_json
