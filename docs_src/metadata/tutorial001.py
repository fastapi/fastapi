from fastapi import FastAPI

app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
