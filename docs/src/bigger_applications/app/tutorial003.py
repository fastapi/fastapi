from fastapi import FastAPI

from .routers.tutorial001 import router as users_router
from .routers.tutorial002 import router as items_router

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router, prefix="/items")
