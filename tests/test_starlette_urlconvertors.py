from fastapi import FastAPI, Path
from starlette.testclient import TestClient

app = FastAPI()


@app.get("/int/{param:int}")
def int_convertor(param: int = Path(...)):
    return {"int": param}


@app.get("/float/{param:float}")
def float_convertor(param: float = Path(...)):
    return {"float": param}


@app.get("/path/{param:path}")
def path_convertor(param: str = Path(...)):
    return {"path": param}


client = TestClient(app)


def test_route_converters_int():
    # Test integer conversion
    response = client.get("/int/5")
    assert response.status_code == 200
    assert response.json() == {"int": 5}
    assert app.url_path_for("int_convertor", param=5) == "/int/5"


def test_route_converters_float():
    # Test float conversion
    response = client.get("/float/25.5")
    assert response.status_code == 200
    assert response.json() == {"float": 25.5}
    assert app.url_path_for("float_convertor", param=25.5) == "/float/25.5"


def test_route_converters_path():
    # Test path conversion
    response = client.get("/path/some/example")
    assert response.status_code == 200
    assert response.json() == {"path": "some/example"}


def test_url_path_for_path_convertor():
    assert (
        app.url_path_for("path_convertor", param="some/example") == "/path/some/example"
    )
