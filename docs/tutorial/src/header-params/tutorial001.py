from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(*, user_agent: str = Header(None)):
    return {"User-Agent": user_agent}
