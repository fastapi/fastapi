from anyio import open_file
from fastapi import Depends, FastAPI
from typing_extensions import Annotated

app = FastAPI()


async def get_username():
    try:
        async with await open_file("/path/to/sanchez.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError:
        print("We didn't re-raise, wubba lubba dub dub!")


@app.get("/me")
def get_me(username: Annotated[str, Depends(get_username)]):
    return username  # pragma: no cover
