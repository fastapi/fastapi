from fastapi import APIRouter, FastAPI, Request
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


@app.middleware("http")
async def app_middleware(request: Request, call_next):
    print("App before")
    response = await call_next(request)
    print("App after")
    return response


async def outer_middleware(request: Request, call_next):
    print("Outer before")
    response = await call_next(request)
    print("Outer after")
    return response


outer = APIRouter(
    prefix="/outer",
    middleware=[Middleware(BaseHTTPMiddleware, dispatch=outer_middleware)],
)


async def name_middleware(request: Request, call_next):
    print(f"Hi {request.path_params.get('name')}!")
    response = await call_next(request)
    print(f"Bye {request.path_params.get('name')}!")
    return response


inner = APIRouter(prefix="/inner")


@inner.get(
    "/{name}",
    middleware=[Middleware(BaseHTTPMiddleware, dispatch=name_middleware)],
)
async def hello(name: str):
    print("Handler")
    return {"message": f"Hello {name} from inner!"}


@outer.get("/")
async def outer_hello():
    print("Handler")
    return {"message": "Hello from outer!"}


@app.get("/")
async def app_hello():
    print("Handler")
    return {"message": "Hello from app!"}


outer.include_router(inner)
app.include_router(outer)
