from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(
    username: str = Form(..., alias="user-name"), password: str = Form(...)
):
    return {"user-name": username}
