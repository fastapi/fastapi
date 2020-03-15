from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str = "default"
    CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"


app = FastAPI()
settings = Settings()


@app.get("/")
async def root():
    # Warning! This example is for demo purposes only.
    # Never expose your secrets.
    return {settings.CLIENT_ID: settings.CLIENT_SECRET}
