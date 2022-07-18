from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(title="White Shuli 2")

@app.get("/pita/shuli")
async def get_shuli_in_a_pita():
    return {"shuli": "pita"}

client = TestClient(app)

def test_swagger_ui():
    response = client.get("/elements")
    assert response.status_code == 200, response.text
    print(response.text)
    assert app.title in response.text
    assert "Stoplight" in response.text

def test_response():
    response = client.get("/pita/shuli")
    assert response.json() == {"shuli": "pita"}
