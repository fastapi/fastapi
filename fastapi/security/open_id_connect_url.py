from typing import Literal, Optional

from fastapi.openapi.models import OpenIdConnect as OpenIdConnectModel
from fastapi.security.base import SecurityBase
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing_extensions import Annotated, Doc, deprecated


class OpenIdConnect(SecurityBase):
    """
    OpenID Connect authentication class. An instance of it would be used as a
    dependency.
    """

    def __init__(
        self,
        *,
        openIdConnectUrl: Annotated[
            str,
            Doc(
                """
            The OpenID Connect URL.
            """
            ),
        ],
        scheme_name: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme name.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme description.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        auto_error: Annotated[
            bool,
            Doc(
                """
                By default, if no HTTP Authorization header is provided, required for
                OpenID Connect authentication, it will automatically cancel the request
                and send the client an error.

                If `auto_error` is set to `False`, when the HTTP Authorization header
                is not available, instead of erroring out, the dependency result will
                be `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, with OpenID
                Connect or in a cookie).
                """
            ),
        ] = True,
        not_authenticated_status_code: Annotated[
            Literal[401, 403],
            Doc(
                """
                By default, if no HTTP Authorization header provided and `auto_error`
                is set to `True`, it will automatically raise an`HTTPException` with
                the status code `401`.

                If your client relies on the old (incorrect) behavior and expects the
                status code to be `403`, you can set `not_authenticated_status_code` to
                `403` to achieve it.

                Keep in mind that this parameter is temporary and will be removed in
                the near future.
                """
            ),
            deprecated(
                """
                This parameter is temporary. It was introduced to give users time
                to upgrade their clients to follow the new behavior and will eventually
                be removed.

                Use it as a short-term workaround, but consider updating your clients
                to align with the new behavior.
                """
            ),
        ] = 401,
    ):
        self.model = OpenIdConnectModel(
            openIdConnectUrl=openIdConnectUrl, description=description
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.not_authenticated_status_code = not_authenticated_status_code

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        if not authorization:
            if self.auto_error:
                if self.not_authenticated_status_code == HTTP_403_FORBIDDEN:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                    )
                else:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Not authenticated",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            else:
                return None
        return authorization
