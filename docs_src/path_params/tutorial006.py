from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
async def read_users():
    return {"user_id": "first behavior"}


@app.get("/users")
async def read_users():
    return {"user_id": "second behavior"}
