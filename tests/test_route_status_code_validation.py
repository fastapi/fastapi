from http import HTTPStatus

import pytest
from fastapi import FastAPI
from fastapi.exceptions import FastAPIError


@pytest.mark.parametrize("status_code", ["20x", "200", "2XX", "default", "ok"])
def test_a_string_status_code_is_rejected_at_declaration(status_code):
    app = FastAPI()

    with pytest.raises(FastAPIError, match="Invalid status_code"):

        @app.get("/x", status_code=status_code)
        def read():
            return {}


def test_an_int_status_code_still_works():
    app = FastAPI()

    @app.get("/x", status_code=201)
    def read():
        return {}

    @app.get("/y", status_code=HTTPStatus.OK)
    def read_ok():
        return {}

    assert app.routes[-2].status_code == 201
    assert app.routes[-1].status_code == 200
