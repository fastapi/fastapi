import uuid
from abc import ABC
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Set

from fastapi import Response, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyCookie, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

try:
    import jwt
except ImportError:  # pragma: nocover
    jwt = None  # type: ignore


class JwtAuthCredentials:
    def __init__(self, subject: Dict[str, Any], jti: str):
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
        assert jwt is not None, "pyjwt must be installed to use JwtAuth"
        assert (
            places is None
            or places == {"header"}
            or places == {"cookie"}
            or places == {"header", "cookie"}
        ), "only 'header', 'cookie' or both supported as token place"
        assert (
            algorithm in jwt.algorithms.get_default_algorithms().keys()  # type: ignore
        ), f"{algorithm} algorithm is not supported by pyjwt library"

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
    def _get_payload(
        subject: Dict[str, Any], expires_delta: timedelta
    ) -> Dict[str, Any]:
        to_encode: Dict[str, Any] = {
            "subject": subject.copy(),  # main subject
            "exp": datetime.utcnow() + expires_delta,  # expire time
            "iat": datetime.utcnow(),  # creation time
            "jti": str(uuid.uuid1()),  # uuid
        }

        return to_encode

    def create_access_token(
        self, subject: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        expires_delta = (
            expires_delta if expires_delta is not None else timedelta(minutes=15)
        )
        to_encode = self._get_payload(subject, expires_delta)

        jwt_encoded = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        # jwt_encoded = jwt_encoded.decode('utf-8')
        return jwt_encoded

    def create_refresh_token(
        self, subject: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        expires_delta = (
            expires_delta if expires_delta is not None else timedelta(days=31)
        )
        to_encode = self._get_payload(subject, expires_delta)

        # Adding creating refresh token mark
        to_encode["type"] = "refresh"

        jwt_encoded = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        # jwt_encoded = jwt_encoded.decode('utf-8')
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


class JwtAuth(JwtAuthBase):
    _access_cookie = JwtAuthBase.JwtAccessCookie()
    _bearer = JwtAuthBase.JwtAccessBearer()

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

    def _get_access_token(
        self,
        bearer: JwtAuthBase.JwtAccessBearer,
        access_cookie: JwtAuthBase.JwtAccessCookie,
    ) -> Optional[str]:
        access_token = None
        if "cookie" in self.places:
            if access_cookie is not None:
                access_token = str(access_cookie)
        if "header" in self.places:
            if bearer is not None:
                access_token = str(bearer.credentials)  # type: ignore

        return access_token

    def __call__(
        self,
        bearer: JwtAuthBase.JwtAccessBearer = Security(_bearer),
        access_cookie: JwtAuthBase.JwtAccessCookie = Security(_access_cookie),
    ) -> Optional[JwtAuthCredentials]:
        access_token = self._get_access_token(bearer, access_cookie)

        # Check token exist
        if access_token is None:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Credentials are not provided"
            )

        # Try to decode jwt token. auto_error on error
        payload = self._decode(access_token)
        if payload is None:
            return None

        # Return JWT token to interact
        return JwtAuthCredentials(payload["subject"], payload["jti"])


class JwtAuthRefresh(JwtAuthBase):
    _refresh_cookie = JwtAuthBase.JwtRefreshCookie()
    _bearer = JwtAuthBase.JwtRefreshBearer()

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

    def _get_refresh_token(
        self,
        bearer: JwtAuthBase.JwtRefreshBearer,
        refresh_cookie: JwtAuthBase.JwtRefreshCookie,
    ) -> Optional[str]:
        refresh_token = None
        if "cookie" in self.places:
            if refresh_cookie is not None:
                refresh_token = str(refresh_cookie)
        if "header" in self.places:
            if bearer is not None:
                refresh_token = str(bearer.credentials)  # type: ignore

        return refresh_token

    def __call__(
        self,
        bearer: JwtAuthBase.JwtRefreshBearer = Security(_bearer),
        refresh_cookie: JwtAuthBase.JwtRefreshCookie = Security(_refresh_cookie),
    ) -> Optional[JwtAuthCredentials]:
        refresh_token = self._get_refresh_token(bearer, refresh_cookie)

        # Check token exist
        if refresh_token is None:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Credentials are not provided"
            )

        # Try to decode jwt token. auto_error on error
        payload = self._decode(refresh_token)
        if payload is None:
            return None

        if "type" not in payload or payload["type"] != "refresh":
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Wrong token: 'type' is not 'refresh'",
            )

        # Return JWT token to interact
        return JwtAuthCredentials(payload["subject"], payload["jti"])


# class JwtAuthRefreshCookie(JwtAuthRefresh):
