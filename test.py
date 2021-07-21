from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient


class Config:
    thing: int
    created: int = 0

    def __init__(self) -> None:
        Config.created += 1
        self.thing = 1


app = FastAPI()


@app.get("/")
def root(cfg: Config = Depends(lifespan="app")):
    ...


with TestClient(app) as client:
    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 200
    assert Config.created == 1
