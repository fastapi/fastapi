from fastapi import FastAPI

from .tutorial01 import router as users_router
from .tutorial02 import router as items_router

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router, prefix="/items")
