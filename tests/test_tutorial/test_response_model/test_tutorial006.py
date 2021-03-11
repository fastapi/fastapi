from fastapi.testclient import TestClient

from docs_src.response_model.tutorial006 import app

client = TestClient(app)


def test_exclude_nested():
    response = client.get("/items/foo/image_name")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "image": {"name": "Some image"},
    }


def test_include_nested():
    response = client.get("/items/foo/image")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "image": {"url": "https://example.com/img.jpg"},
    }


def test_include_nested_index():
    response = client.get("/items/foo/first_video")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "videos": [{"url": "https://example.com/video_1.mp4", "duration": 40}],
    }


def test_include_nested_all():
    response = client.get("/items/foo/videos")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "videos": [
            {"url": "https://example.com/video_1.mp4"},
            {"url": "https://example.com/video_2.mp4"},
        ],
    }
