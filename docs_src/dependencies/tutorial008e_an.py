from fastapi import Depends, FastAPI
from typing_extensions import Annotated

app = FastAPI()


def get_username():
    try:
        yield "Rick"
    finally:
        print("Cleanup up before response is sent")


@app.get("/users/me")
def get_user_me(username: Annotated[str, Depends(get_username, scope="function")]):
    return username
