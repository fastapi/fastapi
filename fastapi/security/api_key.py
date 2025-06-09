from typing import Literal, Optional, Union

from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing_extensions import Annotated, Doc, deprecated


class APIKeyBase(SecurityBase):
    def __init__(
        self,
        location: APIKeyIn,
        name: str,
        description: Union[str, None],
        scheme_name: Union[str, None],
        auto_error: bool,
        not_authenticated_status_code: Literal[401, 403],
    ):
        self.parameter_location = location.value
        self.parameter_name = name
        self.auto_error = auto_error
        self.not_authenticated_status_code = not_authenticated_status_code

        self.model: APIKey = APIKey(
            **{"in": location},  # type: ignore[arg-type]
            name=name,
            description=description,
        )
        self.scheme_name = scheme_name or self.__class__.__name__

    def format_www_authenticate_header_value(self) -> str:
        """
        The WWW-Authenticate header is not standardized for API Key authentication.
        It's considered good practice to include information about the authentication
        challange.
        This method follows one of the common templates.
        If a different format is required, override this method in a subclass.
        """

        return f'ApiKey in="{self.parameter_location}", name="{self.parameter_name}"'

    def check_api_key(self, api_key: Optional[str]) -> Optional[str]:
        if not api_key:
            if self.auto_error:
                if self.not_authenticated_status_code == HTTP_403_FORBIDDEN:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                    )
                else:  # By default use 401
                    www_authenticate = self.format_www_authenticate_header_value()
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Not authenticated",
                        headers={"WWW-Authenticate": www_authenticate},
                    )
            return None
        return api_key


class APIKeyQuery(APIKeyBase):
    """
    API key authentication using a query parameter.

    This defines the name of the query parameter that should be provided in the request
    with the API key and integrates that into the OpenAPI documentation. It extracts
    the key value sent in the query parameter automatically and provides it as the
    dependency result. But it doesn't define how to send that API key to the client.

    ## Usage

    Create an instance object and use that object as the dependency in `Depends()`.

    The dependency result will be a string containing the key value.

    ## Example

    ```python
    from fastapi import Depends, FastAPI
    from fastapi.security import APIKeyQuery

    app = FastAPI()

    query_scheme = APIKeyQuery(name="api_key")


    @app.get("/items/")
    async def read_items(api_key: str = Depends(query_scheme)):
        return {"api_key": api_key}
    ```
    """

    def __init__(
        self,
        *,
        name: Annotated[
            str,
            Doc("Query parameter name."),
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
                By default, if the query parameter is not provided, `APIKeyQuery` will
                automatically cancel the request and send the client an error.

                If `auto_error` is set to `False`, when the query parameter is not
                available, instead of erroring out, the dependency result will be
                `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, in a query
                parameter or in an HTTP Bearer token).
                """
            ),
        ] = True,
        not_authenticated_status_code: Annotated[
            Literal[401, 403],
            Doc(
                """
                By default, if the query parameter is not provided and `auto_error` is
                set to `True`, `APIKeyQuery` will automatically raise an
                `HTTPException` with the status code `401`.

                If your client relies on the old (incorrect) behavior and expects the
                status code to be `403`, you can set `not_authenticated_status_code` to
                `403` to achieve it.

                Keep in mind that this parameter is temporary and will be removed in
                the near future.
                Consider updating your clients to align with the new behavior.
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
        super().__init__(
            location=APIKeyIn.query,
            name=name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
            not_authenticated_status_code=not_authenticated_status_code,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.query_params.get(self.model.name)
        return self.check_api_key(api_key)


class APIKeyHeader(APIKeyBase):
    """
    API key authentication using a header.

    This defines the name of the header that should be provided in the request with
    the API key and integrates that into the OpenAPI documentation. It extracts
    the key value sent in the header automatically and provides it as the dependency
    result. But it doesn't define how to send that key to the client.

    ## Usage

    Create an instance object and use that object as the dependency in `Depends()`.

    The dependency result will be a string containing the key value.

    ## Example

    ```python
    from fastapi import Depends, FastAPI
    from fastapi.security import APIKeyHeader

    app = FastAPI()

    header_scheme = APIKeyHeader(name="x-key")


    @app.get("/items/")
    async def read_items(key: str = Depends(header_scheme)):
        return {"key": key}
    ```
    """

    def __init__(
        self,
        *,
        name: Annotated[str, Doc("Header name.")],
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
                By default, if the header is not provided, `APIKeyHeader` will
                automatically cancel the request and send the client an error.

                If `auto_error` is set to `False`, when the header is not available,
                instead of erroring out, the dependency result will be `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, in a header or
                in an HTTP Bearer token).
                """
            ),
        ] = True,
        not_authenticated_status_code: Annotated[
            Literal[401, 403],
            Doc(
                """
                By default, if the header is not provided and `auto_error` is
                set to `True`, `APIKeyHeader` will automatically raise an
                `HTTPException` with the status code `401`.

                If your client relies on the old (incorrect) behavior and expects the
                status code to be `403`, you can set `not_authenticated_status_code` to
                `403` to achieve it.

                Keep in mind that this parameter is temporary and will be removed in
                the near future.
                Consider updating your clients to align with the new behavior.
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
        super().__init__(
            location=APIKeyIn.header,
            name=name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
            not_authenticated_status_code=not_authenticated_status_code,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        return self.check_api_key(api_key)


class APIKeyCookie(APIKeyBase):
    """
    API key authentication using a cookie.

    This defines the name of the cookie that should be provided in the request with
    the API key and integrates that into the OpenAPI documentation. It extracts
    the key value sent in the cookie automatically and provides it as the dependency
    result. But it doesn't define how to set that cookie.

    ## Usage

    Create an instance object and use that object as the dependency in `Depends()`.

    The dependency result will be a string containing the key value.

    ## Example

    ```python
    from fastapi import Depends, FastAPI
    from fastapi.security import APIKeyCookie

    app = FastAPI()

    cookie_scheme = APIKeyCookie(name="session")


    @app.get("/items/")
    async def read_items(session: str = Depends(cookie_scheme)):
        return {"session": session}
    ```
    """

    def __init__(
        self,
        *,
        name: Annotated[str, Doc("Cookie name.")],
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
                By default, if the cookie is not provided, `APIKeyCookie` will
                automatically cancel the request and send the client an error.

                If `auto_error` is set to `False`, when the cookie is not available,
                instead of erroring out, the dependency result will be `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, in a cookie or
                in an HTTP Bearer token).
                """
            ),
        ] = True,
        not_authenticated_status_code: Annotated[
            Literal[401, 403],
            Doc(
                """
                By default, if the cookie is not provided and `auto_error` is
                set to `True`, `APIKeyCookie` will automatically raise an
                `HTTPException` with the status code `401`.

                If your client relies on the old (incorrect) behavior and expects the
                status code to be `403`, you can set `not_authenticated_status_code` to
                `403` to achieve it.

                Keep in mind that this parameter is temporary and will be removed in
                the near future.
                Consider updating your clients to align with the new behavior.
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
        super().__init__(
            location=APIKeyIn.cookie,
            name=name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
            not_authenticated_status_code=not_authenticated_status_code,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.cookies.get(self.model.name)
        return self.check_api_key(api_key)
