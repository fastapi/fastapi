import typing
from contextlib import contextmanager

from ._client import Client
from ._config import DEFAULT_TIMEOUT_CONFIG
from ._models import Response
from ._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)


def request(
    method: str,
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    follow_redirects: bool = False,
    verify: VerifyTypes = True,
    cert: typing.Optional[CertTypes] = None,
    trust_env: bool = True,
) -> Response:
    """
    Sends an HTTP request.

    **Parameters:**

    * **method** - HTTP method for the new `Request` object: `GET`, `OPTIONS`,
    `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`.
    * **url** - URL for the new `Request` object.
    * **params** - *(optional)* Query parameters to include in the URL, as a
    string, dictionary, or sequence of two-tuples.
    * **content** - *(optional)* Binary content to include in the body of the
    request, as bytes or a byte iterator.
    * **data** - *(optional)* Form data to include in the body of the request,
    as a dictionary.
    * **files** - *(optional)* A dictionary of upload files to include in the
    body of the request.
    * **json** - *(optional)* A JSON serializable object to include in the body
    of the request.
    * **headers** - *(optional)* Dictionary of HTTP headers to include in the
    request.
    * **cookies** - *(optional)* Dictionary of Cookie items to include in the
    request.
    * **auth** - *(optional)* An authentication class to use when sending the
    request.
    * **proxies** - *(optional)* A dictionary mapping proxy keys to proxy URLs.
    * **timeout** - *(optional)* The timeout configuration to use when sending
    the request.
    * **follow_redirects** - *(optional)* Enables or disables HTTP redirects.
    * **verify** - *(optional)* SSL certificates (a.k.a CA bundle) used to
    verify the identity of requested hosts. Either `True` (default CA bundle),
    a path to an SSL certificate file, an `ssl.SSLContext`, or `False`
    (which will disable verification).
    * **cert** - *(optional)* An SSL certificate used by the requested host
    to authenticate the client. Either a path to an SSL certificate file, or
    two-tuple of (certificate file, key file), or a three-tuple of (certificate
    file, key file, password).
    * **trust_env** - *(optional)* Enables or disables usage of environment
    variables for configuration.

    **Returns:** `Response`

    Usage:

    ```
    >>> import httpx
    >>> response = httpx.request('GET', 'https://httpbin.org/get')
    >>> response
    <Response [200 OK]>
    ```
    """
    with Client(
        cookies=cookies,
        proxies=proxies,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    ) as client:
        return client.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )


@contextmanager
def stream(
    method: str,
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    follow_redirects: bool = False,
    verify: VerifyTypes = True,
    cert: typing.Optional[CertTypes] = None,
    trust_env: bool = True,
) -> typing.Iterator[Response]:
    """
    Alternative to `httpx.request()` that streams the response body
    instead of loading it into memory at once.

    **Parameters**: See `httpx.request`.

    See also: [Streaming Responses][0]

    [0]: /quickstart#streaming-responses
    """
    with Client(
        cookies=cookies,
        proxies=proxies,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    ) as client:
        with client.stream(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        ) as response:
            yield response


def get(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `GET` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `GET` requests should not include a request body.
    """
    return request(
        "GET",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def options(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends an `OPTIONS` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `OPTIONS` requests should not include a request body.
    """
    return request(
        "OPTIONS",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def head(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `HEAD` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `HEAD` requests should not include a request body.
    """
    return request(
        "HEAD",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def post(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `POST` request.

    **Parameters**: See `httpx.request`.
    """
    return request(
        "POST",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def put(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `PUT` request.

    **Parameters**: See `httpx.request`.
    """
    return request(
        "PUT",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def patch(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `PATCH` request.

    **Parameters**: See `httpx.request`.
    """
    return request(
        "PATCH",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )


def delete(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = False,
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
) -> Response:
    """
    Sends a `DELETE` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `DELETE` requests should not include a request body.
    """
    return request(
        "DELETE",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    )
