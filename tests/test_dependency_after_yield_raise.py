from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient


class CustomError(Exception):
    pass


def catching_dep() -> Any:
    try:
        yield "s"
    except CustomError as err:
        raise HTTPException(status_code=418, detail="Session error") from err


def broken_dep() -> Any:
    yield "s"
    raise ValueError("Broken after yield")


app = FastAPI()


@app.get("/catching")
def catching(d: Annotated[str, Depends(catching_dep)]) -> Any:
    raise CustomError("Simulated error during streaming")


@app.get("/broken")
def broken(d: Annotated[str, Depends(broken_dep)]) -> Any:
    return {"message": "all good?"}


client = TestClient(app)


def test_catching():
    response = client.get("/catching")
    assert response.status_code == 418
    assert response.json() == {"detail": "Session error"}


def test_broken_raise():
    with pytest.raises(ValueError, match="Broken after yield"):
        client.get("/broken")


def test_broken_no_raise():
    """
    When a dependency with yield raises after the yield (not in an except), the
    response is already "successfully" sent back to the client, but there's still
    an error in the server afterwards, an exception is raised and captured or shown
    in the server logs.
    """
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/broken")
        assert response.status_code == 200
        assert response.json() == {"message": "all good?"}


def test_broken_return_finishes():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/broken")
    assert response.status_code == 200
    assert response.json() == {"message": "all good?"}
