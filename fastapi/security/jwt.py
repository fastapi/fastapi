from abc import ABC
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Set
from uuid import uuid1

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Security
from fastapi.responses import Response
from fastapi.security import APIKeyCookie, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

try:
    from jose import jwt
except ImportError:  # pragma: nocover
    jwt = None


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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        assert jwt is not None, "python-jose must be installed to use JwtAuth"
        if places:
            assert places.issubset(
                {"header", "cookie"}
            ), "only 'header'/'cookie' are supported"
        algorithm = algorithm.upper()
        assert (
            hasattr(jwt.ALGORITHMS, algorithm) is True
        ), f"{algorithm} algorithm is not supported by python-jose library"

        self.secret_key = secret_key

        self.places = {"header"} if places is None else places
        self.auto_error = auto_error
        self.algorithm = algorithm
        self.access_expires_delta = (
            timedelta(minutes=15)
            if access_expires_delta is None
            else access_expires_delta
        )
        self.refresh_expires_delta = (
            timedelta(days=31)
            if refresh_expires_delta is None
            else refresh_expires_delta
        )

    def _decode(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload: Dict[str, Any] = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"leeway": 10},
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=f"Token time expired: {e}"
            )
        except jwt.JWTError as e:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=f"Wrong token: {e}"
            )

    @staticmethod
    def _generate_payload(
        subject: Dict[str, Any], expires_delta: timedelta
    ) -> Dict[str, Any]:
        now = datetime.utcnow()

        to_encode: Dict[str, Any] = {
            "subject": subject.copy(),  # main subject
            "exp": now + expires_delta,  # expire time
            "iat": now,  # creation time
            "jti": str(uuid1()),  # uuid
        }

        return to_encode

    def _get_token(
        self,
        bearer: Optional[HTTPBearer] = None,
        cookie: Optional[APIKeyCookie] = None,
    ) -> Optional[str]:
        if bearer:
            return str(bearer.credentials)  # type: ignore
        if cookie:
            return str(cookie)
        return None

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
            expires_delta if expires_delta is not None else self.access_expires_delta
        )
        to_encode = self._generate_payload(subject, expires_delta)

        jwt_encoded: str = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return jwt_encoded

    def create_refresh_token(
        self, subject: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        expires_delta = (
            expires_delta if expires_delta is not None else self.refresh_expires_delta
        )
        to_encode = self._generate_payload(subject, expires_delta)

        # Adding creating refresh token mark
        to_encode["type"] = "refresh"

        jwt_encoded: str = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return jwt_encoded

    @staticmethod
    def set_access_cookie(
        response: Response, access_token: str, expires_delta: Optional[timedelta] = None
    ) -> None:
        seconds_expires: Optional[int] = (
            int(expires_delta.total_seconds()) if expires_delta else None
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
            int(expires_delta.total_seconds()) if expires_delta else None
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key,
            places=places,
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
        )

    def _get_credentials(
        self,
        bearer: Optional[JwtAuthBase.JwtAccessBearer],
        cookie: Optional[JwtAuthBase.JwtAccessCookie],
    ) -> Optional[JwtAuthorizationCredentials]:
        payload = self._get_payload(bearer, cookie)

        if payload:
            return JwtAuthorizationCredentials(payload["subject"], payload["jti"])
        return None


class JwtAccessBearer(JwtAccess):
    def __init__(
        self,
        secret_key: str,
        auto_error: bool = True,
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header", "cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key,
            places=places,
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
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
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header", "cookie"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
        )

    def __call__(
        self,
        bearer: JwtAuthBase.JwtRefreshBearer = Security(JwtRefresh._bearer),
        cookie: JwtAuthBase.JwtRefreshCookie = Security(JwtRefresh._cookie),
    ) -> Optional[JwtAuthorizationCredentials]:
        return self._get_credentials(bearer=bearer, cookie=cookie)
