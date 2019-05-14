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


def test_swagger_ui_local_fakevalues_default(request, caplog):
    static_directory = os.path.join(request.fspath.dirname, "static")
    custom_keys = ["js", "css", "favicon"]
    for p in range(3):
        for permutation in permutations(custom_keys, p):
            swagger_static = {k: "fakevalue" for k in permutation}
            app = FastAPI(
                static_directory=static_directory, swagger_static=swagger_static
            )

            swagger_keys_test = [x in swagger_static.keys() for x in custom_keys]

            if not all(swagger_keys_test):
                missings = [
                    custom_keys[idx]
                    for idx, x in enumerate(swagger_keys_test)
                    if not x
                ]
                for missing in missings:
                    assert f"Using a static directory and missing {missing} so using default" in caplog.messages
