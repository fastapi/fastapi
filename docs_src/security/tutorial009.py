from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyCookie
from pydantic import BaseModel

app = FastAPI()

api_key = APIKeyCookie(name="key")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(api_key)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
