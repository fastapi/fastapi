from pydantic import BaseModel


class User(BaseModel):
    c: int
