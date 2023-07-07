import binascii
import hashlib
import os
from base64 import b64decode
from typing import Awaitable, Callable, Dict, NoReturn, Optional, Tuple

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import HTTPBase as HTTPBaseModel
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.base import SecurityBase
from fastapi.security.utils import (
    check_nonce,
    digest_access_response,
    get_authorization_scheme_param,
    make_nonce,
)
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


class HTTPBasicCredentials(BaseModel):
    username: str
    password: str


class HTTPAuthorizationCredentials(BaseModel):
    scheme: str
    credentials: str


class HTTPDigestCredentials(BaseModel):
    scheme: str
    credentials: str
    request_method: str
    request_uri: str
    request_body: Callable[[], Awaitable[bytes]]
    username: str
    userhash: bool
    realm: str
    nonce: str
    cnonce: str
    nc: str
    qop: str
    algorithm: Optional[str]

    def _hashed_username(self, username: str) -> str:
        """
        Hash the username if userhash is enabled.
        """
        if self.userhash:
            algo = self.algorithm or "md5"
            algo = (algo[:-5] if algo.endswith("-sess") else algo).lower()
            return hashlib.new(algo, f"{username}:{self.realm}".encode()).hexdigest()
        else:
            return username

    async def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate the credentials against a password.
        """
        if self.username != self._hashed_username(username):
            return False

        return self.credentials == digest_access_response(
            request_method=self.request_method,
            request_uri=self.request_uri,
            request_body=await self.request_body(),
            username=self._hashed_username(username),
            password=password,
            realm=self.realm,
            nonce=self.nonce,
            cnonce=self.cnonce,
            nc=self.nc,
            qop=self.qop,
            algo=self.algorithm,
        )


class HTTPBase(SecurityBase):
    def __init__(
        self,
        *,
        scheme: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBaseModel(scheme=scheme, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


class HTTPBasic(HTTPBase):
    def __init__(
        self,
        *,
        scheme_name: Optional[str] = None,
        realm: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBaseModel(scheme="basic", description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.realm = realm
        self.auto_error = auto_error

    async def __call__(  # type: ignore
        self, request: Request
    ) -> Optional[HTTPBasicCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if self.realm:
            unauthorized_headers = {"WWW-Authenticate": f'Basic realm="{self.realm}"'}
        else:
            unauthorized_headers = {"WWW-Authenticate": "Basic"}
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers=unauthorized_headers,
                )
            else:
                return None
        invalid_user_credentials_exc = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers=unauthorized_headers,
        )
        try:
            data = b64decode(param).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise invalid_user_credentials_exc
        username, separator, password = data.partition(":")
        if not separator:
            raise invalid_user_credentials_exc
        return HTTPBasicCredentials(username=username, password=password)


class HTTPBearer(HTTPBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


class HTTPDigest(HTTPBase):
    def __init__(
        self,
        *,
        scheme_name: Optional[str] = None,
        realm: Optional[str] = None,
        qop: Tuple[str] = ("auth",),
        algorithm: str = "md5",
        userhash: bool = False,
        nonce_secret: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBaseModel(scheme="digest", description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.realm = realm

        self.algorithm_name = (
            algorithm[:-5] if algorithm.endswith("-sess") else algorithm
        ).lower()

        if self.algorithm_name not in hashlib.algorithms_available:
            raise ValueError(f"algorithm must be one of {hashlib.algorithms_available}")
        self.algorithm = algorithm

        if qop != ("auth",):
            raise ValueError("Only 'auth' qop value is supported")
        self.qop = qop

        self.userhash = userhash
        self.nonce_secret = nonce_secret
        self.auto_error = auto_error

        opqaue_data = realm.encode() if realm else os.urandom(32)
        self.opaque = hashlib.new(self.algorithm_name, opqaue_data).hexdigest()

    def _get_unauthorized_headers(
        self, request: Request, stale: bool = False
    ) -> Dict[str, str]:
        header_fields = [
            f'nonce="{make_nonce(request, self.nonce_secret)}"',
            f'opaque="{self.opaque}"',
            f'algorithm="{self.algorithm}"',
            f'qop="{",".join(self.qop)}"',
            f'userhash="{str(self.userhash).lower()}"',
        ]

        if self.realm:
            header_fields.append(f'realm="{self.realm}"')
        if stale:
            header_fields.append('stale="true"')

        return {"WWW-Authenticate": "Digest " + ",".join(header_fields)}

    def _parse_header_as_dict(self, header: str) -> Dict[str, str]:
        return {
            k.strip(): v.strip('" ')
            for k, _, v in (item.partition("=") for item in header.split(","))
        }

    def _error(self, request: Request, detail: str, stale: bool = False) -> NoReturn:
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=detail,
                headers=self._get_unauthorized_headers(request, stale=stale),
            )

        return None  # type: ignore

    async def __call__(  # type: ignore
        self, request: Request
    ) -> Optional[HTTPDigestCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, auth_header = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and auth_header):
            return self._error(request, "Not authenticated")
        if scheme.lower() != "digest":
            return self._error(request, "Invalid authentication credentials")

        parsed_auth = self._parse_header_as_dict(auth_header)

        # Get username details
        # TODO: Handle username with quotes for case userhash is false, and
        #       potentially a 'username*' field.
        username = parsed_auth.get("username")
        if not username:
            return self._error(request, "Invalid username")

        userhash = parsed_auth.get("userhash", "false").lower() == "true"

        # Check realm
        realm = parsed_auth.get("realm")
        if not realm or realm != self.realm:
            return self._error(request, "Invalid realm")

        # Check URI
        uri = parsed_auth.get("uri")
        if uri != request.url.path:
            return self._error(request, "Invalid URI")

        # Check the nonce
        nonce = parsed_auth.get("nonce")
        if not nonce or not check_nonce(nonce, request, secret=self.nonce_secret):
            return self._error(request, "Stale nonce", stale=True)

        # Checp qop
        qop = parsed_auth.get("qop")
        if qop not in self.qop:
            return self._error(request, "Unsupported QOP")

        # Check cnonce
        cnonce = parsed_auth.get("cnonce")
        if not cnonce:
            return self._error(request, "Invalid authentication credentials")

        # TODO: Consider handling nonce-counter
        nc = parsed_auth.get("nc")
        if not nc:
            return self._error(request, "Invalid authentication credentials")

        # Check the response
        response = parsed_auth.get("response")
        if not response:
            return self._error(request, "Invalid authentication credentials")

        return HTTPDigestCredentials(
            scheme=scheme,
            credentials=response,
            request_method=request.method,
            request_uri=request.url.path,
            request_body=request.body,
            username=username,
            userhash=userhash,
            realm=realm,
            nonce=nonce,
            cnonce=cnonce,
            nc=nc,
            qop=qop,
            algorithm=self.algorithm,
        )
