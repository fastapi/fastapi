from fastapi import Depends, FastAPI, Response


def dependency(response: Response) -> None:
    # set the status code for the path operation
    response.status_code = 404
    yield 1234
    # this is not the same object as `response` above
    final_response = response.final_response
    assert final_response is not response
    # you can log or otherwise use the response,
    # but you can't change it anymore
    assert final_response.body == b"1234"


app = FastAPI()

@app.get("/")
def root(response: Response, value: int = Depends(dependency)) -> int:
    assert response.status_code == 404  # set by the dependency
    return value  # FastAPI will implicitly create a new JSONResponse
