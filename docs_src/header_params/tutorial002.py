from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(strange_header: str = Header(None, convert_underscores=False)):
    return {"strange_header": strange_header}
