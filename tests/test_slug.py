from fastapi import FastAPI, Path
from starlette.requests import Request
from starlette.testclient import TestClient

app = FastAPI()


@app.get("/myblog/posts/{id}/{slug:path}")
async def view_post(request: Request, id: int = Path(...), slug: str = Path(...)):
    return dict(request.path_params)


client = TestClient(app)


def test_slug():
    response = client.get("myblog/posts/42/my_article_is_very_insightful/escaped")
    assert response.status_code == 200
    assert response.json() == {
        "id": "42",
        "slug": "my_article_is_very_insightful/escaped",
    }

    response = client.get(
        "myblog/posts/42/my_article_is_very_insightful/this_could_be_anything/whatever"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "42",
        "slug": "my_article_is_very_insightful/this_could_be_anything/whatever",
    }
