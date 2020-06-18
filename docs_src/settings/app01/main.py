from fastapi import FastAPI

from . import config

app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": config.settings.app_name,
        "admin_email": config.settings.admin_email,
        "items_per_user": config.settings.items_per_user,
    }
