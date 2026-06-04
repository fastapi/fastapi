from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me() -> dict:
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str) -> dict:
    return {"user_id": user_id}
