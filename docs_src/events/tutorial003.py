from fastapi import FastAPI


async def lifespan(app):
    print("startup")
    yield
    print("shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    return {"result": "hello world"}
