from fastapi import FastAPI

app = FastAPI(
    title="My Super Project",
    version="2.5.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
