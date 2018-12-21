from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(*, username: str = Form(...), password: str = Form(...)):
    return {"username": username}
