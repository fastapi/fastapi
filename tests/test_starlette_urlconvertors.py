from fastapi import FastAPI, Path, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/int/{param:int}")
def int_convertor(param: int = Path()):
    return {"int": param}


@app.get("/float/{param:float}")
def float_convertor(param: float = Path()):
    return {"float": param}


@app.get("/path/{param:path}")
def path_convertor(param: str = Path()):
    return {"path": param}


@app.get("/query/")
def query_convertor(param: str = Query()):
    return {"query": param}


client = TestClient(app)


def test_route_converters_int():
    # Test integer conversion
    response = client.get("/int/5")
    assert response.status_code == 200, response.text
    assert response.json() == {"int": 5}
    assert app.url_path_for("int_convertor", param=5) == "/int/5"  # type: ignore


def test_route_converters_float():
    # Test float conversion
    response = client.get("/float/25.5")
    assert response.status_code == 200, response.text
    assert response.json() == {"float": 25.5}
    assert app.url_path_for("float_convertor", param=25.5) == "/float/25.5"  # type: ignore


def test_route_converters_path():
    # Test path conversion
    response = client.get("/path/some/example")
    assert response.status_code == 200, response.text
    assert response.json() == {"path": "some/example"}


def test_route_converters_query():
    # Test query conversion
    response = client.get("/query", params={"param": "Qué tal!"})
    assert response.status_code == 200, response.text
    assert response.json() == {"query": "Qué tal!"}


def test_url_path_for_path_convertor():
    assert (
        app.url_path_for("path_convertor", param="some/example") == "/path/some/example"
    )
