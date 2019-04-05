from fastapi import FastAPI

from .routers import items, users

app = FastAPI()

app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)
