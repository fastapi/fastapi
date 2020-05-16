from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"


settings = Settings()

app = FastAPI(openapi_url=settings.openapi_url)


@app.get("/")
def root():
    return {"message": "Hello World"}
