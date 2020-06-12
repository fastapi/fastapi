from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}
