import functools
import json
import sys
import typing

import click
import httpcore
import pygments.lexers
import pygments.util
import rich.console
import rich.markup
import rich.progress
import rich.syntax
import rich.table

from ._client import Client
from ._exceptions import RequestError
from ._models import Response
from ._status_codes import codes


def print_help() -> None:
    console = rich.console.Console()

    console.print("[bold]HTTPX :butterfly:", justify="center")
    console.print()
    console.print("A next generation HTTP client.", justify="center")
    console.print()
    console.print(
        "Usage: [bold]httpx[/bold] [cyan]<URL> [OPTIONS][/cyan] ", justify="left"
    )
    console.print()

    table = rich.table.Table.grid(padding=1, pad_edge=True)
    table.add_column("Parameter", no_wrap=True, justify="left", style="bold")
    table.add_column("Description")
    table.add_row(
        "-m, --method [cyan]METHOD",
        "Request method, such as GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD.\n"
        "[Default: GET, or POST if a request body is included]",
    )
    table.add_row(
        "-p, --params [cyan]<NAME VALUE> ...",
        "Query parameters to include in the request URL.",
    )
    table.add_row(
        "-c, --content [cyan]TEXT", "Byte content to include in the request body."
    )
    table.add_row(
        "-d, --data [cyan]<NAME VALUE> ...", "Form data to include in the request body."
    )
    table.add_row(
        "-f, --files [cyan]<NAME FILENAME> ...",
        "Form files to include in the request body.",
    )
    table.add_row("-j, --json [cyan]TEXT", "JSON data to include in the request body.")
    table.add_row(
        "-h, --headers [cyan]<NAME VALUE> ...",
        "Include additional HTTP headers in the request.",
    )
    table.add_row(
        "--cookies [cyan]<NAME VALUE> ...", "Cookies to include in the request."
    )
    table.add_row(
        "--auth [cyan]<USER PASS>",
        "Username and password to include in the request. Specify '-' for the password to use "
        "a password prompt. Note that using --verbose/-v will expose the Authorization "
        "header, including the password encoding in a trivially reversible format.",
    )

    table.add_row(
        "--proxies [cyan]URL",
        "Send the request via a proxy. Should be the URL giving the proxy address.",
    )

    table.add_row(
        "--timeout [cyan]FLOAT",
        "Timeout value to use for network operations, such as establishing the connection, "
        "reading some data, etc... [Default: 5.0]",
    )

    table.add_row("--follow-redirects", "Automatically follow redirects.")
    table.add_row("--no-verify", "Disable SSL verification.")
    table.add_row(
        "--http2", "Send the request using HTTP/2, if the remote server supports it."
    )

    table.add_row(
        "--download [cyan]FILE",
        "Save the response content as a file, rather than displaying it.",
    )

    table.add_row("-v, --verbose", "Verbose output. Show request as well as response.")
    table.add_row("--help", "Show this message and exit.")
    console.print(table)


def get_lexer_for_response(response: Response) -> str:
    content_type = response.headers.get("Content-Type")
    if content_type is not None:
        mime_type, _, _ = content_type.partition(";")
        try:
            return typing.cast(
                str, pygments.lexers.get_lexer_for_mimetype(mime_type.strip()).name
            )
        except pygments.util.ClassNotFound:  # pragma: no cover
            pass
    return ""  # pragma: no cover


def format_request_headers(request: httpcore.Request, http2: bool = False) -> str:
    version = "HTTP/2" if http2 else "HTTP/1.1"
    headers = [
        (name.lower() if http2 else name, value) for name, value in request.headers
    ]
    method = request.method.decode("ascii")
    target = request.url.target.decode("ascii")
    lines = [f"{method} {target} {version}"] + [
        f"{name.decode('ascii')}: {value.decode('ascii')}" for name, value in headers
    ]
    return "\n".join(lines)


def format_response_headers(
    http_version: bytes,
    status: int,
    reason_phrase: typing.Optional[bytes],
    headers: typing.List[typing.Tuple[bytes, bytes]],
) -> str:
    version = http_version.decode("ascii")
    reason = (
        codes.get_reason_phrase(status)
        if reason_phrase is None
        else reason_phrase.decode("ascii")
    )
    lines = [f"{version} {status} {reason}"] + [
        f"{name.decode('ascii')}: {value.decode('ascii')}" for name, value in headers
    ]
    return "\n".join(lines)


def print_request_headers(request: httpcore.Request, http2: bool = False) -> None:
    console = rich.console.Console()
    http_text = format_request_headers(request, http2=http2)
    syntax = rich.syntax.Syntax(http_text, "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)
    syntax = rich.syntax.Syntax("", "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)


def print_response_headers(
    http_version: bytes,
    status: int,
    reason_phrase: typing.Optional[bytes],
    headers: typing.List[typing.Tuple[bytes, bytes]],
) -> None:
    console = rich.console.Console()
    http_text = format_response_headers(http_version, status, reason_phrase, headers)
    syntax = rich.syntax.Syntax(http_text, "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)
    syntax = rich.syntax.Syntax("", "http", theme="ansi_dark", word_wrap=True)
    console.print(syntax)


def print_response(response: Response) -> None:
    console = rich.console.Console()
    lexer_name = get_lexer_for_response(response)
    if lexer_name:
        if lexer_name.lower() == "json":
            try:
                data = response.json()
                text = json.dumps(data, indent=4)
            except ValueError:  # pragma: no cover
                text = response.text
        else:
            text = response.text

        syntax = rich.syntax.Syntax(text, lexer_name, theme="ansi_dark", word_wrap=True)
        console.print(syntax)
    else:
        console.print(f"<{len(response.content)} bytes of binary data>")


_PCTRTT = typing.Tuple[typing.Tuple[str, str], ...]
_PCTRTTT = typing.Tuple[_PCTRTT, ...]
_PeerCertRetDictType = typing.Dict[str, typing.Union[str, _PCTRTTT, _PCTRTT]]


def format_certificate(cert: _PeerCertRetDictType) -> str:  # pragma: no cover
    lines = []
    for key, value in cert.items():
        if isinstance(value, (list, tuple)):
            lines.append(f"*   {key}:")
            for item in value:
                if key in ("subject", "issuer"):
                    for sub_item in item:
                        lines.append(f"*     {sub_item[0]}: {sub_item[1]!r}")
                elif isinstance(item, tuple) and len(item) == 2:
                    lines.append(f"*     {item[0]}: {item[1]!r}")
                else:
                    lines.append(f"*     {item!r}")
        else:
            lines.append(f"*   {key}: {value!r}")
    return "\n".join(lines)


def trace(
    name: str, info: typing.Mapping[str, typing.Any], verbose: bool = False
) -> None:
    console = rich.console.Console()
    if name == "connection.connect_tcp.started" and verbose:
        host = info["host"]
        console.print(f"* Connecting to {host!r}")
    elif name == "connection.connect_tcp.complete" and verbose:
        stream = info["return_value"]
        server_addr = stream.get_extra_info("server_addr")
        console.print(f"* Connected to {server_addr[0]!r} on port {server_addr[1]}")
    elif name == "connection.start_tls.complete" and verbose:  # pragma: no cover
        stream = info["return_value"]
        ssl_object = stream.get_extra_info("ssl_object")
        version = ssl_object.version()
        cipher = ssl_object.cipher()
        server_cert = ssl_object.getpeercert()
        alpn = ssl_object.selected_alpn_protocol()
        console.print(f"* SSL established using {version!r} / {cipher[0]!r}")
        console.print(f"* Selected ALPN protocol: {alpn!r}")
        if server_cert:
            console.print("* Server certificate:")
            console.print(format_certificate(server_cert))
    elif name == "http11.send_request_headers.started" and verbose:
        request = info["request"]
        print_request_headers(request, http2=False)
    elif name == "http2.send_request_headers.started" and verbose:  # pragma: no cover
        request = info["request"]
        print_request_headers(request, http2=True)
    elif name == "http11.receive_response_headers.complete":
        http_version, status, reason_phrase, headers = info["return_value"]
        print_response_headers(http_version, status, reason_phrase, headers)
    elif name == "http2.receive_response_headers.complete":  # pragma: no cover
        status, headers = info["return_value"]
        http_version = b"HTTP/2"
        reason_phrase = None
        print_response_headers(http_version, status, reason_phrase, headers)


def download_response(response: Response, download: typing.BinaryIO) -> None:
    console = rich.console.Console()
    console.print()
    content_length = response.headers.get("Content-Length")
    with rich.progress.Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(bar_width=None),
        rich.progress.DownloadColumn(),
        rich.progress.TransferSpeedColumn(),
    ) as progress:
        description = f"Downloading [bold]{rich.markup.escape(download.name)}"
        download_task = progress.add_task(
            description,
            total=int(content_length or 0),
            start=content_length is not None,
        )
        for chunk in response.iter_bytes():
            download.write(chunk)
            progress.update(download_task, completed=response.num_bytes_downloaded)


def validate_json(
    ctx: click.Context,
    param: typing.Union[click.Option, click.Parameter],
    value: typing.Any,
) -> typing.Any:
    if value is None:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:  # pragma: no cover
        raise click.BadParameter("Not valid JSON")


def validate_auth(
    ctx: click.Context,
    param: typing.Union[click.Option, click.Parameter],
    value: typing.Any,
) -> typing.Any:
    if value == (None, None):
        return None

    username, password = value
    if password == "-":  # pragma: no cover
        password = click.prompt("Password", hide_input=True)
    return (username, password)


def handle_help(
    ctx: click.Context,
    param: typing.Union[click.Option, click.Parameter],
    value: typing.Any,
) -> None:
    if not value or ctx.resilient_parsing:
        return

    print_help()
    ctx.exit()


@click.command(add_help_option=False)
@click.argument("url", type=str)
@click.option(
    "--method",
    "-m",
    "method",
    type=str,
    help=(
        "Request method, such as GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD. "
        "[Default: GET, or POST if a request body is included]"
    ),
)
@click.option(
    "--params",
    "-p",
    "params",
    type=(str, str),
    multiple=True,
    help="Query parameters to include in the request URL.",
)
@click.option(
    "--content",
    "-c",
    "content",
    type=str,
    help="Byte content to include in the request body.",
)
@click.option(
    "--data",
    "-d",
    "data",
    type=(str, str),
    multiple=True,
    help="Form data to include in the request body.",
)
@click.option(
    "--files",
    "-f",
    "files",
    type=(str, click.File(mode="rb")),
    multiple=True,
    help="Form files to include in the request body.",
)
@click.option(
    "--json",
    "-j",
    "json",
    type=str,
    callback=validate_json,
    help="JSON data to include in the request body.",
)
@click.option(
    "--headers",
    "-h",
    "headers",
    type=(str, str),
    multiple=True,
    help="Include additional HTTP headers in the request.",
)
@click.option(
    "--cookies",
    "cookies",
    type=(str, str),
    multiple=True,
    help="Cookies to include in the request.",
)
@click.option(
    "--auth",
    "auth",
    type=(str, str),
    default=(None, None),
    callback=validate_auth,
    help=(
        "Username and password to include in the request. "
        "Specify '-' for the password to use a password prompt. "
        "Note that using --verbose/-v will expose the Authorization header, "
        "including the password encoding in a trivially reversible format."
    ),
)
@click.option(
    "--proxies",
    "proxies",
    type=str,
    default=None,
    help="Send the request via a proxy. Should be the URL giving the proxy address.",
)
@click.option(
    "--timeout",
    "timeout",
    type=float,
    default=5.0,
    help=(
        "Timeout value to use for network operations, such as establishing the "
        "connection, reading some data, etc... [Default: 5.0]"
    ),
)
@click.option(
    "--follow-redirects",
    "follow_redirects",
    is_flag=True,
    default=False,
    help="Automatically follow redirects.",
)
@click.option(
    "--no-verify",
    "verify",
    is_flag=True,
    default=True,
    help="Disable SSL verification.",
)
@click.option(
    "--http2",
    "http2",
    type=bool,
    is_flag=True,
    default=False,
    help="Send the request using HTTP/2, if the remote server supports it.",
)
@click.option(
    "--download",
    type=click.File("wb"),
    help="Save the response content as a file, rather than displaying it.",
)
@click.option(
    "--verbose",
    "-v",
    type=bool,
    is_flag=True,
    default=False,
    help="Verbose. Show request as well as response.",
)
@click.option(
    "--help",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=handle_help,
    help="Show this message and exit.",
)
def main(
    url: str,
    method: str,
    params: typing.List[typing.Tuple[str, str]],
    content: str,
    data: typing.List[typing.Tuple[str, str]],
    files: typing.List[typing.Tuple[str, click.File]],
    json: str,
    headers: typing.List[typing.Tuple[str, str]],
    cookies: typing.List[typing.Tuple[str, str]],
    auth: typing.Optional[typing.Tuple[str, str]],
    proxies: str,
    timeout: float,
    follow_redirects: bool,
    verify: bool,
    http2: bool,
    download: typing.Optional[typing.BinaryIO],
    verbose: bool,
) -> None:
    """
    An HTTP command line client.
    Sends a request and displays the response.
    """
    if not method:
        method = "POST" if content or data or files or json else "GET"

    try:
        with Client(
            proxies=proxies,
            timeout=timeout,
            verify=verify,
            http2=http2,
        ) as client:
            with client.stream(
                method,
                url,
                params=list(params),
                content=content,
                data=dict(data),
                files=files,  # type: ignore
                json=json,
                headers=headers,
                cookies=dict(cookies),
                auth=auth,
                follow_redirects=follow_redirects,
                extensions={"trace": functools.partial(trace, verbose=verbose)},
            ) as response:
                if download is not None:
                    download_response(response, download)
                else:
                    response.read()
                    if response.content:
                        print_response(response)

    except RequestError as exc:
        console = rich.console.Console()
        console.print(f"[red]{type(exc).__name__}[/red]: {exc}")
        sys.exit(1)

    sys.exit(0 if response.is_success else 1)
