import pytest
from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient


@pytest.fixture()
def framework():
    app = FastAPI()
    tag1 = APIRouter(tags=["tag1"])
    tag2 = APIRouter(tags=["tag2", "tag1"])
    tag3 = APIRouter(tags=["tag2", "tag1"])
    tag4 = APIRouter(tags=["tag4"])

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

    @tag4.get("/get", tags=["tag4get"])
    async def tag4_get():
        return {"Tag": "tag4"}

    @tag4.put("/put", tags=["tag4put"])
    async def tag4_put():
        return {"Tag": "tag4"}

    @tag4.post("/post", tags=["tag4post"])
    async def tag4_post():
        return {"Tag": "tag4"}

    @tag4.delete("/delete", tags=["tag4delete"])
    async def tag4_delete():
        return {"Tag": "tag4"}

    @tag4.options("/options", tags=["tag4options"])
    async def tag4_options():
        return {"Tag": "tag4"}

    @tag4.head("/head", tags=["tag4head"])
    async def tag4_head():
        return {"Tag": "tag4"}

    @tag4.patch("/patch", tags=["tag4patch"])
    async def tag4_patch():
        return {"Tag": "tag4"}

    @tag4.trace("/trace", tags=["tag4trace"])
    async def tag4_trace():
        return {"Tag": "tag4"}

    app.include_router(tag1, prefix="/tag1prefix")
    app.include_router(tag2, prefix="/tag2prefix")
    app.include_router(tag3, prefix="/tag3prefix")
    app.include_router(tag4, prefix="/tag4prefix")

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
    (
        "tag4",
        ["get", "put", "post", "delete", "options", "patch", "trace"],
        [],
        {"Tag": "tag4"},
    ),
]


@pytest.mark.parametrize("tag, methods, expected_tags, expected_json", data)
def test_tags_in_schema(framework, tag, methods, expected_tags, expected_json):
    with TestClient(framework) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        if tag in ["tag1", "tag2", "tag3"]:
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
        elif tag == "tag4":
            for method in methods:
                expected_tags = ["tag4"]
                expected_tags.append(f"tag4{method}")
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
