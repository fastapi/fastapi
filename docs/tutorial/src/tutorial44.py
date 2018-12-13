from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(*, accept_encoding: str = Header(None)):
    return {"Accept-Encoding": accept_encoding}
