import uuid
from abc import ABC
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Set

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Security
from fastapi.responses import Response
from fastapi.security import APIKeyCookie, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

try:
    import jwt
except ImportError:  # pragma: nocover
    jwt = None  # type: ignore


class JwtAuthorizationCredentials:
    def __init__(self, subject: Dict[str, Any], jti: Optional[str] = None):
        self.subject = subject
        self.jti = jti

    def __getitem__(self, item: str) -> Any:
        return self.subject[item]


class JwtAuthBase(ABC):
    class JwtAccessCookie(APIKeyCookie):
        def __init__(self, *args: Any, **kwargs: Any):
            APIKeyCookie.__init__(
                self, *args, name="access_token_cookie", auto_error=False, **kwargs
            )

    class JwtRefreshCookie(APIKeyCookie):
        def __init__(self, *args: Any, **kwargs: Any):
            APIKeyCookie.__init__(
                self, *args, name="refresh_token_cookie", auto_error=False, **kwargs
            )

    class JwtAccessBearer(HTTPBearer):
        def __init__(self, *args: Any, **kwargs: Any):
            HTTPBearer.__init__(self, *args, auto_error=False, **kwargs)

    class JwtRefreshBearer(HTTPBearer):
        def __init__(self, *args: Any, **kwargs: Any):
            HTTPBearer.__init__(self, *args, auto_error=False, **kwargs)

    def __init__(
        self,
        secret_key: str,
        places: Optional[Set[str]] = None,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        assert jwt is not None, "PyJWT must be installed to use JwtAuth"
        if places:
            for i in places:
                assert i in {"header", "cookie"}, "only 'header'/'cookie' are supported"
        assert (
            algorithm in jwt.algorithms.get_default_algorithms().keys()  # type: ignore
        ), f"{algorithm} algorithm is not supported by PyJWT library"

        self.secret_key = secret_key

        self.places = {"header"} if places is None else places
        self.auto_error = auto_error
        self.algorithm = algorithm

    def _decode(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm], leeway=10
            )
        except jwt.ExpiredSignatureError as e:
            if not self.auto_error:
                return None
            raise HTTPException(status_code=401, detail=f"Token time expired: {e}")
        except jwt.InvalidTokenError as e:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=f"Wrong token: {e}"
            )

        # if "subject" not in payload:
        #     if not self.auto_error:
        #         return None
        #     raise HTTPException(
        #         status_code=HTTP_401_UNAUTHORIZED,
        #         detail="Wrong token: 'subject' not in payload",
        #     )

        return payload

    @staticmethod
    def _generate_payload(
        subject: Dict[str, Any], expires_delta: timedelta
    ) -> Dict[str, Any]:
        now = datetime.utcnow()

        to_encode: Dict[str, Any] = {
            "subject": subject.copy(),  # main subject
            "exp": now + expires_delta,  # expire time
            "iat": now,  # creation time
            "jti": str(uuid.uuid1()),  # uuid
        }

        return to_encode

    def _get_token(
        self,
        bearer: Optional[HTTPBearer],
        cookie: Optional[APIKeyCookie],
    ) -> Optional[str]:
        token = None

        if cookie is not None:
            token = str(cookie)
        if bearer is not None:
            token = str(bearer.credentials)  # type: ignore

        return token

    def _get_payload(
        self, bearer: Optional[HTTPBearer], cookie: Optional[APIKeyCookie]
    ) -> Optional[Dict[str, Any]]:
        refresh_token = self._get_token(bearer, cookie)  # TODO: del function

        # Check token exist
        if refresh_token is None:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Credentials are not provided"
            )

        # Try to decode jwt token. auto_error on error
        payload = self._decode(refresh_token)
        return payload

    def create_access_token(
        self, subject: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        expires_delta = (
            expires_delta if expires_delta is not None else timedelta(minutes=15)
        )
        to_encode = self._generate_payload(subject, expires_delta)

        jwt_encoded = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return jwt_encoded

    def create_refresh_token(
        self, subject: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        expires_delta = (
            expires_delta if expires_delta is not None else timedelta(days=31)
        )
        to_encode = self._generate_payload(subject, expires_delta)

        # Adding creating refresh token mark
        to_encode["type"] = "refresh"

        jwt_encoded = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return jwt_encoded

    @staticmethod
    def set_access_cookie(
        response: Response, access_token: str, expires_delta: Optional[timedelta] = None
    ) -> None:
        seconds_expires: Optional[int] = (
            int(expires_delta.total_seconds()) if expires_delta is not None else None
        )
        response.set_cookie(
            key="access_token_cookie",
            value=access_token,
            httponly=False,
            max_age=seconds_expires,  # type: ignore
        )

    @staticmethod
    def set_refresh_cookie(
        response: Response,
        refresh_token: str,
        expires_delta: Optional[timedelta] = None,
    ) -> None:
        seconds_expires: Optional[int] = (
            int(expires_delta.total_seconds()) if expires_delta is not None else None
        )
        response.set_cookie(
            key="refresh_token_cookie",
            value=refresh_token,
            httponly=True,
            max_age=seconds_expires,  # type: ignore
        )

    @staticmethod
    def unset_access_cookie(response: Response) -> None:
        response.set_cookie(
            key="access_token_cookie", value="", httponly=False, max_age=-1
        )

    @staticmethod
    def unset_refresh_cookie(response: Response) -> None:
        response.set_cookie(
            key="refresh_token_cookie", value="", httponly=True, max_age=-1
        )


class JwtAccess(JwtAuthBase):
    _bearer = JwtAuthBase.JwtAccessBearer()
    _cookie = JwtAuthBase.JwtAccessCookie()

    def __init__(
        self,
        secret_key: str,
        places: Optional[Set[str]] = None,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key, places=places, auto_error=auto_error, algorithm=algorithm
        )

    def _get_credentials(
        self,
        bearer: Optional[JwtAuthBase.JwtAccessBearer],
        cookie: Optional[JwtAuthBase.JwtAccessCookie],
    ) -> Optional[JwtAuthorizationCredentials]:
        payload = self._get_payload(bearer, cookie)

        if payload is None:
            return None

        return JwtAuthorizationCredentials(payload["subject"], payload["jti"])


class JwtAccessBearer(JwtAccess):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header"},
            auto_error=auto_error,
            algorithm=algorithm,
        )

    def __call__(
        self, bearer: JwtAuthBase.JwtAccessBearer = Security(JwtAccess._bearer)
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=bearer, cookie=None)


class JwtAccessCookie(JwtAccess):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key=secret_key,
            places={"cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
        )

    def __call__(
        self,
        cookie: JwtAuthBase.JwtAccessCookie = Security(JwtAccess._cookie),
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=None, cookie=cookie)


class JwtAccessBearerCookie(JwtAccess):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header", "cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
        )

    def __call__(
        self,
        bearer: JwtAuthBase.JwtAccessBearer = Security(JwtAccess._bearer),
        cookie: JwtAuthBase.JwtAccessCookie = Security(JwtAccess._cookie),
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=bearer, cookie=cookie)


class JwtRefresh(JwtAuthBase):
    _bearer = JwtAuthBase.JwtRefreshBearer()
    _cookie = JwtAuthBase.JwtRefreshCookie()

    def __init__(
        self,
        secret_key: str,
        places: Optional[Set[str]] = None,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key, places=places, auto_error=auto_error, algorithm=algorithm
        )

    def _get_credentials(
        self,
        bearer: Optional[JwtAuthBase.JwtRefreshBearer],
        cookie: Optional[JwtAuthBase.JwtRefreshCookie],
    ) -> Optional[JwtAuthorizationCredentials]:
        payload = self._get_payload(bearer, cookie)

        if payload is None:
            return None

        if "type" not in payload or payload["type"] != "refresh":
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Wrong token: 'type' is not 'refresh'",
            )

        return JwtAuthorizationCredentials(payload["subject"], payload["jti"])


class JwtRefreshBearer(JwtRefresh):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header"},
            auto_error=auto_error,
            algorithm=algorithm,
        )

    def __call__(
        self, bearer: JwtAuthBase.JwtRefreshBearer = Security(JwtRefresh._bearer)
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=bearer, cookie=None)


class JwtRefreshCookie(JwtRefresh):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key=secret_key,
            places={"cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
        )

    def __call__(
        self,
        cookie: JwtAuthBase.JwtRefreshCookie = Security(JwtRefresh._cookie),
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=None, cookie=cookie)


class JwtRefreshBearerCookie(JwtRefresh):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = "HS256",
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header", "cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
        )

    def __call__(
        self,
        bearer: JwtAuthBase.JwtRefreshBearer = Security(JwtRefresh._bearer),
        cookie: JwtAuthBase.JwtRefreshCookie = Security(JwtRefresh._cookie),
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=bearer, cookie=cookie)
