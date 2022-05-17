from fastapi import Depends, FastAPI, Header, HTTPException, Request

app = FastAPI()


async def verify_token(x_token: str = Header(default=None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(default=None)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items(request: Request):
    return [{"item": "Foo"}, {"item": "Bar"}]
