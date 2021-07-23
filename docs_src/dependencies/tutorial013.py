from fastapi import Depends, FastAPI
from pydantic import BaseSettings


class Config(BaseSettings):
    app_name: str = "AwesomeAPI"


def get_config() -> Config:
    return Config()


async def startup(cfg: Config = Depends(get_config)):
    print("I am ", cfg.app_name)


app = FastAPI(on_startup=[startup])
