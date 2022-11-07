import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RouteAlreadyExistsError


def test_app_router_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()

        @app.get("/items/")
        def read_items():
            return

        @app.get("/items/")
        def read_items2():
            return


def test_sub_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @router.get("/items/")
        def read_items():
            return

        @router.get("/items/")
        def read_items2():
            return

        app.include_router(router)


def test_mix_app_sub_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @app.get("/items/")
        def read_items():
            return

        @router.get("/items/")
        def read_items2():
            return

        app.include_router(router)


def test_sub_route_direct_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @router.route("/items/")
        def read_items():
            return

        @router.route("/items/")
        def read_items2():
            return

        app.include_router(router)


def test_app_router_with_duplicate_path_different_method():
    app = FastAPI()

    @app.get("/items/")
    def read_items():
        return

    @app.post("/items/")
    def read_items2():
        return


def test_sub_with_duplicate_path_different_method():
    app = FastAPI()
    router = APIRouter()

    @router.get("/items/")
    def read_items():
        return

    @router.post("/items/")
    def read_items2():
        return

    app.include_router(router)


def test_mix_app_sub_with_duplicate_different_method():
    app = FastAPI()
    router = APIRouter()

    @app.get("/items/")
    def read_items():
        return

    @router.post("/items/")
    def read_items2():
        return

    app.include_router(router)


def test_sub_route_direct_duplicate_path_different_method():
    app = FastAPI()
    router = APIRouter()

    @router.route("/items/")
    def read_items():
        return

    @router.route("/items/", methods=["POST"])
    def read_items2():
        return

    app.include_router(router)
