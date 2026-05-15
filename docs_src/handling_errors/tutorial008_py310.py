from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def global_unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Global handler: {exc.name} did something."},
    )


magic_router = APIRouter(prefix="/magic")


@magic_router.get("/unicorns/{name}")
async def read_magic_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


def custom_unicorn_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Special handler: {exc.name} did something magical!"},
    )


special_router = APIRouter(
    prefix="/special",
    exception_handlers={UnicornException: custom_unicorn_handler},
)


@special_router.get("/unicorns/{name}")
async def read_special_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


app.include_router(magic_router)
app.include_router(special_router)
