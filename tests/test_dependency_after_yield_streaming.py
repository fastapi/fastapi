from contextlib import contextmanager
from typing import Annotated, Any, Generator

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient


class Session:
    def __init__(self) -> None:
        self.data = ["foo", "bar", "baz"]
        self.open = True

    def __iter__(self) -> Generator[str, None, None]:
        for item in self.data:
            if self.open:
                yield item
            else:
                raise ValueError("Session closed")


@contextmanager
def acquire_session() -> Generator[Session, None, None]:
    session = Session()
    try:
        yield session
    finally:
        session.open = False


def dep_session() -> Any:
    with acquire_session() as s:
        yield s


SessionDep = Annotated[Session, Depends(dep_session)]

app = FastAPI()


@app.get("/data")
def get_data(session: SessionDep) -> Any:
    data = list(session)
    return data


@app.get("/stream-simple")
def get_stream_simple(session: SessionDep) -> Any:
    def iter_data():
        yield from ["x", "y", "z"]

    return StreamingResponse(iter_data())


@app.get("/stream-session")
def get_stream_session(session: SessionDep) -> Any:
    def iter_data():
        yield from session

    return StreamingResponse(iter_data())


def session_explode() -> None:
    with acquire_session() as s:
        iter_s = iter(s)
        print(next(iter_s))
    print(next(iter_s))


client = TestClient(app)


def test_stream_simple():
    response = client.get("/stream-simple")
    assert response.text == "xyz"


def test_stream_session():
    response = client.get("/stream-session")
    assert response.text == "foobarbaz"
