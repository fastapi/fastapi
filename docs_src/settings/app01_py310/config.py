from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
