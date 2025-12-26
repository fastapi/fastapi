import importlib
from types import ModuleType
from typing import Annotated, Any
from unittest.mock import Mock, patch

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(
    name="module",
    params=[
        "tutorial008_py39",
        # Fails with `NameError: name 'DepA' is not defined`
        pytest.param("tutorial008_an_py39", marks=pytest.mark.xfail),
    ],
)
def get_module(request: pytest.FixtureRequest):
    mod_name = f"docs_src.dependencies.{request.param}"
    mod = importlib.import_module(mod_name)
    return mod


def test_get_db(module: ModuleType):
    app = FastAPI()

    @app.get("/")
    def read_root(c: Annotated[Any, Depends(module.dependency_c)]):
        return {"c": str(c)}

    client = TestClient(app)

    a_mock = Mock()
    b_mock = Mock()
    c_mock = Mock()

    with (
        patch(
            f"{module.__name__}.generate_dep_a",
            return_value=a_mock,
            create=True,
        ),
        patch(
            f"{module.__name__}.generate_dep_b",
            return_value=b_mock,
            create=True,
        ),
        patch(
            f"{module.__name__}.generate_dep_c",
            return_value=c_mock,
            create=True,
        ),
    ):
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"c": str(c_mock)}
