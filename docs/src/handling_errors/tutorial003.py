from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/")
async def root():
    return {"message": "Hello World"}
