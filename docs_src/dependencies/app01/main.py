from fastapi import Depends, FastAPI
from fastapi.dependencies.lifetime import DependencyLifetime

from . import config

app = FastAPI()


def get_settings():
    return config.Settings()


@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings, lifetime=DependencyLifetime.app)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
