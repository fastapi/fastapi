from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


router = APIRouter(
    prefix="/unicorns",
    exception_handlers={
        UnicornException: lambda request, exc: JSONResponse(
            status_code=418,
            content={
                "message": f"Oops! {exc.name} did something. There goes a rainbow..."
            },
        )
    },
)


@router.get("/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


app = FastAPI()
app.include_router(router)
