from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()


async def response_status_setter(response: Response):
    response.status_code = 201


async def parent_dep(result=Depends(response_status_setter)):
    return result


@app.get("/", dependencies=[Depends(parent_dep)])
async def get_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_dependency_set_status_code():
    response = client.get("/")
    assert response.status_code == 201, response.text
    assert response.json() == {"msg": "Hello World"}
