import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RouteAlreadyExistsError


def test_app_router_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()

        @app.get("/items/")
        def read_items():
            return  # pragma: no cover

        @app.get("/items/")
        def read_items2():
            return  # pragma: no cover


def test_sub_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @router.get("/items/")
        def read_items():
            return  # pragma: no cover

        @router.get("/items/")
        def read_items2():
            return  # pragma: no cover

        app.include_router(router)  # pragma: no cover


def test_mix_app_sub_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @app.get("/items/")
        def read_items():
            return  # pragma: no cover

        @router.get("/items/")
        def read_items2():
            return  # pragma: no cover

        app.include_router(router)  # pragma: no cover


def test_sub_route_direct_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @router.route("/items/")
        def read_items():
            return  # pragma: no cover

        @router.route("/items/")
        def read_items2():
            return  # pragma: no cover

        app.include_router(router)  # pragma: no cover


def test_app_router_with_duplicate_path_different_method():
    app = FastAPI()

    @app.get("/items/")
    def read_items():
        return  # pragma: no cover

    @app.post("/items/")
    def read_items2():
        return  # pragma: no cover


def test_sub_with_duplicate_path_different_method():
    app = FastAPI()
    router = APIRouter()

    @router.get("/items/")
    def read_items():
        return  # pragma: no cover

    @router.post("/items/")
    def read_items2():
        return  # pragma: no cover

    app.include_router(router)  # pragma: no cover


def test_mix_app_sub_with_duplicate_different_method():
    app = FastAPI()
    router = APIRouter()

    @app.get("/items/")
    def read_items():
        return  # pragma: no cover

    @router.post("/items/")
    def read_items2():
        return  # pragma: no cover

    app.include_router(router)  # pragma: no cover


def test_sub_route_direct_duplicate_path_different_method():
    app = FastAPI()
    router = APIRouter()

    @router.route("/items/")
    def read_items():
        return  # pragma: no cover

    @router.route("/items/", methods=["POST"])
    def read_items2():
        return  # pragma: no cover

    app.include_router(router)  # pragma: no cover


def test_app_websocket_route_with_duplicate_path():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()

        @app.websocket("/items/")
        def read_items():
            return  # pragma: no cover

        @app.websocket("/items/")
        def read_items2():
            return  # pragma: no cover


def test_sub_with_duplicate_path_with_prefix():
    with pytest.raises(RouteAlreadyExistsError):
        app = FastAPI()
        router = APIRouter()

        @router.get("/items/")
        def read_items():
            return  # pragma: no cover

        @router.get("/items/")
        def read_items2():
            return  # pragma: no cover

        app.include_router(router, prefix="/prefix")  # pragma: no cover

