from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", openapi_extra={"x-aperture-labs-portal": "blue"})
async def read_items():
    return [{"item_id": "portal-gun"}]
