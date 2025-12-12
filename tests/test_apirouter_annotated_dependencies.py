from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient
from typing_extensions import Annotated


def get_value() -> int:
    return 1


ValueDep = Annotated[int, Depends(get_value)]


router = APIRouter(dependencies=[Depends(lambda: "sdfgh"), ValueDep])


@router.get("/")
def read_root(dep: ValueDep):
    return {"dep": dep}


@router.get("/no_dep")
def no_dep():
    return {"status": 200}


app = FastAPI()
app.include_router(router)

router.post("/", dependencies=[Depends(lambda: None)])


def test_apirouter_annotated_dependencies():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"dep": 1}

    response = client.get("/no_dep")
    assert response.status_code == 200
    assert response.json() == {"status": 200}
