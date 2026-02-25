# Ref: https://github.com/fastapi/fastapi/discussions/6024#discussioncomment-8541913


from typing import Annotated

import pytest
from fastapi import Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


@pytest.fixture(name="call_counts")
def call_counts_fixture():
    return {
        "get_db_session": 0,
        "get_current_user": 0,
        "get_user_me": 0,
        "get_user_items": 0,
    }


@pytest.fixture(name="app")
def app_fixture(call_counts: dict[str, int]):
    def get_db_session():
        call_counts["get_db_session"] += 1
        return f"db_session_{call_counts['get_db_session']}"

    def get_current_user(
        security_scopes: SecurityScopes,
        db_session: Annotated[str, Depends(get_db_session)],
    ):
        call_counts["get_current_user"] += 1
        return {
            "user": f"user_{call_counts['get_current_user']}",
            "scopes": security_scopes.scopes,
            "db_session": db_session,
        }

    def get_user_me(
        current_user: Annotated[dict, Security(get_current_user, scopes=["me"])],
    ):
        call_counts["get_user_me"] += 1
        return {
            "user_me": f"user_me_{call_counts['get_user_me']}",
            "current_user": current_user,
        }

    def get_user_items(
        user_me: Annotated[dict, Depends(get_user_me)],
    ):
        call_counts["get_user_items"] += 1
        return {
            "user_items": f"user_items_{call_counts['get_user_items']}",
            "user_me": user_me,
        }

    app = FastAPI()

    @app.get("/")
    def path_operation(
        user_me: Annotated[dict, Depends(get_user_me)],
        user_items: Annotated[dict, Security(get_user_items, scopes=["items"])],
    ):
        return {
            "user_me": user_me,
            "user_items": user_items,
        }

    return app


@pytest.fixture(name="client")
def client_fixture(app: FastAPI):
    return TestClient(app)


def test_security_scopes_sub_dependency_caching(
    client: TestClient, call_counts: dict[str, int]
):
    response = client.get("/")

    assert response.status_code == 200
    assert call_counts["get_db_session"] == 1
    assert call_counts["get_current_user"] == 2
    assert call_counts["get_user_me"] == 2
    assert call_counts["get_user_items"] == 1
    assert response.json() == {
        "user_me": {
            "user_me": "user_me_1",
            "current_user": {
                "user": "user_1",
                "scopes": ["me"],
                "db_session": "db_session_1",
            },
        },
        "user_items": {
            "user_items": "user_items_1",
            "user_me": {
                "user_me": "user_me_2",
                "current_user": {
                    "user": "user_2",
                    "scopes": ["items", "me"],
                    "db_session": "db_session_1",
                },
            },
        },
    }
