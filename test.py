from fastapi import FastAPI, Depends


def get_db():
    try:
        yield
    finally:
        pass

app = FastAPI()

@app.get("/")
def root(dep: None = Depends(get_db)):
    ...


from fastapi.testclient import TestClient

TestClient(app).get("/")
