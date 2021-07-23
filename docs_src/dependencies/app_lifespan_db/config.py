from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql://user:password@postgresserver/db"


def get_config() -> Settings:
    return Settings()
