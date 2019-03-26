import os
from itertools import permutations

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

swagger_static_js = "swagger-ui-bundle.js"
swagger_static_css = "swagger-ui.css"
swagger_static_icon = "favicon.png"


def test_swagger_ui_local(request):
    static_directory = os.path.join(request.fspath.dirname, "static")
    app = FastAPI(
        static_directory=static_directory,
        swagger_static={
            "js": swagger_static_js,
            "css": swagger_static_css,
            "favicon": swagger_static_icon,
        },
    )
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert swagger_static_js in response.text
    for static_file in [swagger_static_js, swagger_static_css, swagger_static_icon]:
        response = client.get("/static/" + static_file)
        assert response.status_code == 200


def test_swagger_ui_local_no_extra(request):
    static_directory = os.path.join(request.fspath.dirname, "static")
    required_keys = ["js", "css", "favicon"]
    for p in range(3):
        for permutation in permutations(required_keys, p):
            with pytest.raises(ValueError) as e:
                swagger_static = {k: "fakevalue" for k in permutation}
                app = FastAPI(
                    static_directory=static_directory, swagger_static=swagger_static
                )
            assert (
                str(e.value)
                == f"The swagger_static dict needs to be passed to extra, missing {[i for i in required_keys if i not in permutation]}"
            )
