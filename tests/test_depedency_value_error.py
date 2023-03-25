from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def validate_text(text: str):
    if "bad_word" in text:
        raise ValueError("bad_word is not allowed")

    return {"error": False, "message": "success"}


@app.get("/text")
async def validate_text(text: dict = Depends(validate_text)):
    return text


client = TestClient(app)


def test_normal_text():
    response = client.get("/text?text=hello_world")
    assert response.status_code == 200, response.text
    assert response.json() == {"error": False, "message": "success"}


def test_bad_text():
    response = client.get("/text?text=bad_word")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "text"],
                "msg": "bad_word is not allowed",
                "type": "value_error",
            }
        ]
    }
