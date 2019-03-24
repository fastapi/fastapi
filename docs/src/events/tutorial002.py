from fastapi import FastAPI

app = FastAPI()


@app.on_event("shutdown")
def startup_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
