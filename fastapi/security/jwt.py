import binascii
from base64 import b64decode
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import HTTPBase as HTTPBaseModel
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

import typing as tp
from datetime import datetime, timedelta
import uuid
from abc import ABC

from fastapi import Security, Response
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, APIKeyCookie

try:
    import jwt
except ImportError:  # pragma: nocover
    jwt = None  # type: ignore


class JwtAuthCredentials:
    def __init__(self, subject: dict[str, tp.Any], jti: str):
        self.subject = subject
        self.jti = jti

    def __getitem__(self, item: str) -> tp.Any:
        return self.subject[item]

    @staticmethod
    def _get_payload(subject: dict[str, tp.Any], expires_delta: timedelta) -> dict[str, tp.Any]:
        to_encode: dict[str, tp.Any] = {
            'subject': subject.copy(),  # main subject
            'exp': datetime.utcnow() + expires_delta,  # expire time
            'iat': datetime.utcnow(),  # creation time
            'jti': str(uuid.uuid1()),  # uuid
        }

        return to_encode

    @staticmethod
    def create_access_token(subject: dict[str, tp.Any], expires_delta: tp.Optional[timedelta] = None) -> str:
        expires_delta = (expires_delta if expires_delta is not None else timedelta(minutes=15))
        to_encode = JwtAuthCredentials._get_payload(subject, expires_delta)

        jwt_encoded = jwt.encode(to_encode, settings.jwt_secret_key, algorithm='HS256')
        if isinstance(jwt_encoded, bytes):  # type: ignore
            return jwt_encoded.decode('utf-8')  # type: ignore
        return jwt_encoded

    @staticmethod
    def create_refresh_token(subject: dict[str, tp.Any], expires_delta: tp.Optional[timedelta] = None) -> str:
        expires_delta = (expires_delta if expires_delta is not None else timedelta(days=31))
        to_encode = JwtAuthCredentials._get_payload(subject, expires_delta)

        # Adding creating refresh token mark
        to_encode['type'] = 'refresh'

        jwt_encoded = jwt.encode(to_encode, settings.jwt_secret_key, algorithm='HS256')
        if isinstance(jwt_encoded, bytes):  # type: ignore
            return jwt_encoded.decode('utf-8')  # type: ignore
        return jwt_encoded

    @staticmethod
    def set_access_cookies(response: Response, access_token: str, expires_delta: tp.Optional[timedelta] = None) -> None:
        seconds_expires = int(expires_delta.total_seconds() + 10) if expires_delta is not None else None
        response.set_cookie(key='access_token_cookie', value=access_token,
                            httponly=False, max_age=seconds_expires)  # type: ignore

    @staticmethod
    def unset_access_cookies(response: Response) -> None:
        response.set_cookie(key='access_token_cookie', value='', httponly=False, max_age=-1)

    @staticmethod
    def set_refresh_cookies(response: Response, refresh_token: str,
                            expires_delta: tp.Optional[timedelta] = None) -> None:
        seconds_expires = int(expires_delta.total_seconds() + 10) if expires_delta is not None else None
        response.set_cookie(key='refresh_token_cookie', value=refresh_token,
                            httponly=True, max_age=seconds_expires)  # type: ignore

    @staticmethod
    def unset_refresh_cookies(response: Response) -> None:
        response.set_cookie(key='refresh_token_cookie', value='', httponly=True, max_age=-1)


class JwtAuthBase(ABC):
    class JwtAccessCookie(APIKeyCookie):
        def __init__(self, *args: tp.Any, **kwargs: tp.Any):
            APIKeyCookie.__init__(self, *args, name='access_token_cookie', auto_error=False, **kwargs)

    class JwtRefreshCookie(APIKeyCookie):
        def __init__(self, *args: tp.Any, **kwargs: tp.Any):
            APIKeyCookie.__init__(self, *args, name='refresh_token_cookie', auto_error=False, **kwargs)

    class JwtBearer(HTTPBearer):
        def __init__(self, *args: tp.Any, **kwargs: tp.Any):
            HTTPBearer.__init__(self, *args, auto_error=False, **kwargs)

    def __init__(self, place: tp.Optional[set[str]] = None, auto_error: bool = True):
        assert jwt is not None, "jwt must be installed to use JwtAuth"

        self.place = {'header'} if place is None else place
        self.auto_error = auto_error

    def _get_payload(self, token: str) -> tp.Optional[dict[str, tp.Any]]:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=['HS256'], leeway=10)
        except jwt.ExpiredSignatureError as e:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=419,
                detail=f"Token time expired: {e}"
            )
        except jwt.InvalidTokenError as e:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=401,
                detail=f"Wrong token: {e}"
            )

        if 'subject' not in payload:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=401,
                detail="Wrong token: 'subject' not in payload"
            )

        return payload


class JwtAuth(JwtAuthBase):
    _access_cookie = JwtAuthBase.JwtAccessCookie()
    _bearer = JwtAuthBase.JwtBearer()

    def __init__(self, place: tp.Optional[set[str]] = None, auto_error: bool = True):
        super().__init__(place, auto_error)

    def _get_access_token(self, bearer: JwtAuthBase.JwtBearer = Security(_bearer),
                          access_cookie: JwtAuthBase.JwtAccessCookie = Security(_access_cookie)) -> tp.Optional[str]:
        access_token = None
        if 'cookie' in self.place:
            if access_cookie is not None:
                access_token = str(access_cookie)
        if 'header' in self.place:
            if bearer is not None:
                access_token = str(bearer.credentials)  # type: ignore

        return access_token

    def __call__(self, bearer: JwtAuthBase.JwtBearer = Security(_bearer),
                 access_cookie: JwtAuthBase.JwtAccessCookie = Security(_access_cookie)
                 ) -> tp.Optional[JwtAuthCredentials]:
        access_token = self._get_access_token(bearer, access_cookie)

        # Check token exist
        if access_token is None:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=401,
                detail="Credential are not provided"
            )

        # Try to decode jwt token. auto_error on error
        payload = self._get_payload(access_token)
        if payload is None:
            return None

        # Return JWT token to interact
        return JwtAuthCredentials(payload['subject'], payload['jti'])


class JwtAuthRefresh(JwtAuthBase):
    _refresh_cookie = JwtAuthBase.JwtRefreshCookie()
    _bearer = JwtAuthBase.JwtBearer()

    def __init__(self, place: tp.Optional[set[str]] = None, auto_error: bool = True):
        super().__init__(place, auto_error)

    def _get_refresh_token(self, bearer: JwtAuthBase.JwtBearer = Security(_bearer),
                           refresh_cookie: JwtAuthBase.JwtRefreshCookie = Security(_refresh_cookie)
                           ) -> tp.Optional[str]:
        refresh_token = None
        if 'cookie' in self.place:
            if refresh_cookie is not None:
                refresh_token = str(refresh_cookie)
        if 'header' in self.place:
            if bearer is not None:
                refresh_token = str(bearer.credentials)  # type: ignore

        return refresh_token

    def __call__(self, bearer: JwtAuthBase.JwtBearer = Security(_bearer),
                 refresh_cookie: JwtAuthBase.JwtRefreshCookie = Security(_refresh_cookie)
                 ) -> tp.Optional[JwtAuthCredentials]:
        refresh_token = self._get_refresh_token(bearer, refresh_cookie)

        # Check token exist
        if refresh_token is None:
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=401,
                detail="Credential are not provided"
            )

        # Try to decode jwt token. auto_error on error
        payload = self._get_payload(refresh_token)
        if payload is None:
            return None

        if 'type' not in payload or payload['type'] != 'refresh':
            if not self.auto_error:
                return None
            raise HTTPException(
                status_code=401,
                detail="Wrong token: 'type' is not 'refresh'"
            )

        # Return JWT token to interact
        return JwtAuthCredentials(payload['subject'], payload['jti'])
