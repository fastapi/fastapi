from fastapi import FastAPI, Form
from starlette.testclient import TestClient


app:FastAPI = FastAPI()

@app.post("/testing_alias")
async def check_alias(id_test: int = Form(alias="otherId")):
    return {"other_id":id_test}

@app.patch("/testing")
async def check_without_alias(id_test:int = Form()):
    return {"id_test":id_test}


client = TestClient(app)

def test_without_alias():
    response = client.patch("/testing", data={"id_test":1})
    assert response.status_code == 200
    assert response.json() == {"id_test":1}

def test_get_alias():
    response = client.post("/testing_alias", data={"otherId":"1"})
    assert response.status_code == 200
    assert response.json() == {"other_id":1}