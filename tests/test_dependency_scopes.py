from unittest.mock import Mock, call, patch

import pytest
from fastapi import APIRouter, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


def app_security(scopes: SecurityScopes):
    _app_security(scopes.scopes)


def app_scope_disabler(scopes: SecurityScopes):
    active = set()
    for scope in scopes.scopes:
        if not scope.startswith("-"):
            active.add(scope)
        else:
            active.discard(scope[1:])
    _app_scope_disabler(sorted(active))


def _app_security(scopes):  # pragma: no cover
    pass


def _app_scope_disabler(scopes):  # pragma: no cover
    pass


@pytest.fixture
def mocks():
    with patch.dict(
        globals(), {"_app_security": Mock(), "_app_scope_disabler": Mock()}
    ):
        yield


app = FastAPI(
    dependencies=[
        Security(app_security, scopes=["b", "a"]),
        Security(app_scope_disabler, scopes=["b", "a", "-c"]),
    ]
)

router1 = APIRouter()


@app.get("/root")
def root():
    return {}


@router1.get("/router1")
def get_router1():
    return {}


app.include_router(
    router1,
    dependencies=[
        Security(app_security, scopes=["b", "c"]),
        Security(app_scope_disabler, scopes=["-b", "c"]),
    ],
)

client = TestClient(app)


def test_repr():
    security = Security(
        app_security,
        scopes=[
            "a",
            "b",
        ],
    )
    assert repr(security) == "Security(app_security, scopes=['a', 'b'])"


def test_root(mocks):
    client.get("root_disabled")
    _app_security.assert_not_called()
    client.get("root")
    _app_security.assert_has_calls(
        [
            call(["b", "a"]),
        ]
    )


def test_router1(mocks):
    client.get("router1")
    _app_security.assert_has_calls(
        [
            call(["b", "a", "b", "c"]),
        ]
    )


def test_root_scope_disabler(mocks):
    client.get("root")
    _app_scope_disabler.assert_has_calls(
        [
            call(["a", "b"]),
        ]
    )


def test_router1_scope_disabler(mocks):
    client.get("router1")
    _app_scope_disabler.assert_has_calls(
        [
            call(["a", "c"]),
        ]
    )
