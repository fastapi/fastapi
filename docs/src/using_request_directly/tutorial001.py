from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
