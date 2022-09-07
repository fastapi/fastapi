from fastapi import FastAPI, Response
from fastapi.params import Path
from fastapi.testclient import TestClient

msg = {"msg": "Status overwritten"}

app = FastAPI()


@app.delete(
    "/{id}",
    responses={
        204: {"model": None, "description": "No Content"},
    },
    status_code=204,
)
async def delete_deployment(
    id: str = Path(None),
    response: Response = None,
) -> None:
    response.status_code = 400
    return msg


client = TestClient(app)


def test_dependency_set_status_code():
    response = client.delete("/1")
    assert response.status_code == 400 and response.content
    assert response.json() == msg
