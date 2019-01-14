from fastapi import FastAPI

from .routers.items import router as items_router
from .routers.users import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router, prefix="/items")
