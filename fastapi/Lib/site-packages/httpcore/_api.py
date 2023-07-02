from contextlib import contextmanager
from typing import Iterator, Optional, Union

from ._models import URL, Extensions, HeaderTypes, Response
from ._sync.connection_pool import ConnectionPool


def request(
    method: Union[bytes, str],
    url: Union[URL, bytes, str],
    *,
    headers: HeaderTypes = None,
    content: Union[bytes, Iterator[bytes], None] = None,
    extensions: Optional[Extensions] = None,
) -> Response:
    """
    Sends an HTTP request, returning the response.

    ```
    response = httpcore.request("GET", "https://www.example.com/")
    ```

    Arguments:
        method: The HTTP method for the request. Typically one of `"GET"`,
            `"OPTIONS"`, `"HEAD"`, `"POST"`, `"PUT"`, `"PATCH"`, or `"DELETE"`.
        url: The URL of the HTTP request. Either as an instance of `httpcore.URL`,
            or as str/bytes.
        headers: The HTTP request headers. Either as a dictionary of str/bytes,
            or as a list of two-tuples of str/bytes.
        content: The content of the request body. Either as bytes,
            or as a bytes iterator.
        extensions: A dictionary of optional extra information included on the request.
            Possible keys include `"timeout"`.

    Returns:
        An instance of `httpcore.Response`.
    """
    with ConnectionPool() as pool:
        return pool.request(
            method=method,
            url=url,
            headers=headers,
            content=content,
            extensions=extensions,
        )


@contextmanager
def stream(
    method: Union[bytes, str],
    url: Union[URL, bytes, str],
    *,
    headers: HeaderTypes = None,
    content: Union[bytes, Iterator[bytes], None] = None,
    extensions: Optional[Extensions] = None,
) -> Iterator[Response]:
    """
    Sends an HTTP request, returning the response within a content manager.

    ```
    with httpcore.stream("GET", "https://www.example.com/") as response:
        ...
    ```

    When using the `stream()` function, the body of the response will not be
    automatically read. If you want to access the response body you should
    either use `content = response.read()`, or `for chunk in response.iter_content()`.

    Arguments:
        method: The HTTP method for the request. Typically one of `"GET"`,
            `"OPTIONS"`, `"HEAD"`, `"POST"`, `"PUT"`, `"PATCH"`, or `"DELETE"`.
        url: The URL of the HTTP request. Either as an instance of `httpcore.URL`,
            or as str/bytes.
        headers: The HTTP request headers. Either as a dictionary of str/bytes,
            or as a list of two-tuples of str/bytes.
        content: The content of the request body. Either as bytes,
            or as a bytes iterator.
        extensions: A dictionary of optional extra information included on the request.
            Possible keys include `"timeout"`.

    Returns:
        An instance of `httpcore.Response`.
    """
    with ConnectionPool() as pool:
        with pool.stream(
            method=method,
            url=url,
            headers=headers,
            content=content,
            extensions=extensions,
        ) as response:
            yield response
