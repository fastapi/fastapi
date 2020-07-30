from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="This is my API, with auto docs for the API and everything",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "John Doe",
        "url": "http://example.com/contact/",
        "email": "johndoe@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
