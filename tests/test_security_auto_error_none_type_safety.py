from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import (
    APIKeyCookie,
    APIKeyHeader,
    APIKeyQuery,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from fastapi.testclient import TestClient


def test_oauth2_non_optional_no_auth():
    app = FastAPI()
    oauth2 = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @app.get("/me")
    def get_me(token: str = Depends(oauth2)):
        return {"token": token}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/me")
    assert resp.status_code == 500
    assert "non-optional" in resp.json()["detail"]


def test_oauth2_optional_no_auth():
    app = FastAPI()
    oauth2 = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @app.get("/me")
    def get_me(token: str | None = Depends(oauth2)):
        return {"token": token}

    client = TestClient(app)
    resp = client.get("/me")
    assert resp.status_code == 200
    assert resp.json() == {"token": None}


def test_oauth2_non_optional_with_auth():
    app = FastAPI()
    oauth2 = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @app.get("/me")
    def get_me(token: str = Depends(oauth2)):
        return {"token": token}

    client = TestClient(app)
    resp = client.get("/me", headers={"Authorization": "Bearer valid"})
    assert resp.status_code == 200
    assert resp.json() == {"token": "valid"}


def test_http_bearer_non_optional_no_auth():
    app = FastAPI()
    bearer = HTTPBearer(auto_error=False)

    @app.get("/profile")
    def get_profile(creds: HTTPAuthorizationCredentials = Depends(bearer)):
        return {"scheme": creds.scheme}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/profile")
    assert resp.status_code == 500


def test_http_bearer_optional_no_auth():
    app = FastAPI()
    bearer = HTTPBearer(auto_error=False)

    @app.get("/profile")
    def get_profile(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if creds is None:
            return {"status": "anonymous"}
        return {"scheme": creds.scheme}

    client = TestClient(app)
    resp = client.get("/profile")
    assert resp.status_code == 200
    assert resp.json() == {"status": "anonymous"}


def test_api_key_header_non_optional_no_key():
    app = FastAPI()
    api_key = APIKeyHeader(name="X-API-Key", auto_error=False)

    @app.get("/data")
    def get_data(key: str = Depends(api_key)):
        return {"key": key}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/data")
    assert resp.status_code == 500


def test_api_key_query_non_optional_no_key():
    app = FastAPI()
    api_key = APIKeyQuery(name="api_key", auto_error=False)

    @app.get("/data")
    def get_data(key: str = Depends(api_key)):
        return {"key": key}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/data")
    assert resp.status_code == 500


def test_api_key_cookie_non_optional_no_key():
    app = FastAPI()
    api_key = APIKeyCookie(name="session", auto_error=False)

    @app.get("/data")
    def get_data(key: str = Depends(api_key)):
        return {"key": key}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/data")
    assert resp.status_code == 500


def test_http_basic_non_optional_no_auth():
    app = FastAPI()
    basic = HTTPBasic(auto_error=False)

    @app.get("/data")
    def get_data(creds: HTTPBasicCredentials = Depends(basic)):
        return {"user": creds.username}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/data")
    assert resp.status_code == 500


def test_annotated_syntax_non_optional():
    app = FastAPI()
    api_key = APIKeyHeader(name="X-API-Key", auto_error=False)

    @app.get("/data")
    def get_data(key: Annotated[str, Depends(api_key)]):
        return {"key": key}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/data")
    assert resp.status_code == 500

    resp2 = client.get("/data", headers={"X-API-Key": "secret"})
    assert resp2.status_code == 200
    assert resp2.json() == {"key": "secret"}


def test_annotated_syntax_optional():
    app = FastAPI()
    api_key = APIKeyHeader(name="X-API-Key", auto_error=False)

    @app.get("/data")
    def get_data(key: Annotated[str | None, Depends(api_key)]):
        return {"key": key}

    client = TestClient(app)
    resp = client.get("/data")
    assert resp.status_code == 200
    assert resp.json() == {"key": None}


def test_any_annotation_allows_none():
    """Any annotation should allow None (no type constraint)."""
    from typing import Any

    app = FastAPI()
    oauth2 = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @app.get("/me")
    def get_me(token: Any = Depends(oauth2)):
        return {"token": token}

    client = TestClient(app)
    resp = client.get("/me")
    assert resp.status_code == 200
    assert resp.json() == {"token": None}


def test_none_type_annotation_allows_none():
    app = FastAPI()
    oauth2 = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @app.get("/me")
    def get_me(token: None = Depends(oauth2)):
        return {"token": token}

    client = TestClient(app)
    resp = client.get("/me")
    assert resp.status_code == 200
    assert resp.json() == {"token": None}


def test_annotated_non_optional_inner_blocked():
    """Annotated[str, Depends(...)] should still be blocked when str is non-optional."""
    from typing import Annotated

    app = FastAPI()
    api_key = APIKeyHeader(name="X-Key", auto_error=False)

    @app.get("/data")
    def get_data(key: Annotated[str, Depends(api_key)]):
        return {"key": key}

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/data")
    assert resp.status_code == 500


def test_annotated_optional_inner_allowed():
    """Annotated[str | None, Depends(...)] should allow None."""
    from typing import Annotated

    app = FastAPI()
    api_key = APIKeyHeader(name="X-Key", auto_error=False)

    @app.get("/data")
    def get_data(key: Annotated[str | None, Depends(api_key)]):
        return {"key": key}

    client = TestClient(app)
    resp = client.get("/data")
    assert resp.status_code == 200
    assert resp.json() == {"key": None}


def test_chain_through_intermediate_not_blocked():
    app = FastAPI()
    oauth2 = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    def get_user(token: str | None = Depends(oauth2)):
        if token is None:
            return None
        return {"name": "alice"}

    @app.get("/data")
    def get_data(user: dict = Depends(get_user)):
        if user is None:
            return {"msg": "anonymous"}
        return user

    client = TestClient(app)
    resp = client.get("/data")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "anonymous"}
