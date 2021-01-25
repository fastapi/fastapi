from starlette.responses import PlainTextResponse

from fastapi import Depends, HTTPException, FastAPI

app = FastAPI()


class MyCustomException(Exception):
    pass


@app.exception_handler(MyCustomException)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


async def dependency():
    try:
        yield
    except MyCustomException:
        pass


@app.get(
    "/raise-my-custom-exception",
    dependencies=[Depends(dependency, exit_before_response=True)],
)
async def read_items():
    raise MyCustomException()
