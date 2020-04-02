from fastapi import Depends, FastAPI

from . import config

app = FastAPI()


def get_settings():
    if config.settings:
        return config.settings
    config.settings = config.Settings()
    return config.settings


@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
