from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED

app = FastAPI()


@app.post("/items/", status_code=HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
