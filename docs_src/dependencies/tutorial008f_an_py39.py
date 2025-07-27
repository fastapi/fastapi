from typing import Annotated

from anyio import open_file
from fastapi import Depends, FastAPI

app = FastAPI()


async def get_username():
    try:
        async with await open_file("/path/to/sanchez.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError:
        print("We don't swallow the OS error here, we raise again 😎")
        raise


@app.get("/me")
def get_me(username: Annotated[str, Depends(get_username)]):
    return username  # pragma: no cover
