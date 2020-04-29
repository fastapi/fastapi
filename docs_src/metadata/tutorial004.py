from fastapi import FastAPI

tag_description = [
    {"name": "foo", "description": "This is the description for tag FOO"},
    {
        "name": "bar",
        "description": "This is the description for tag BAR",
        "externalDocs": {
            "description": "External documentation",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tag_description)


@app.get("/foo", tags=["foo"])
async def get_foo():
    return {"id": "foo"}


@app.get("/bar", tags=["bar"])
async def get_bar():
    return {"id": "bar"}
