from http import HTTPStatus

import pytest

from .._events import (
    ConnectionClosed,
    Data,
    EndOfMessage,
    InformationalResponse,
    Request,
    Response,
)
from .._util import LocalProtocolError


def test_events() -> None:
    with pytest.raises(LocalProtocolError):
        # Missing Host:
        req = Request(
            method="GET", target="/", headers=[("a", "b")], http_version="1.1"
        )
    # But this is okay (HTTP/1.0)
    req = Request(method="GET", target="/", headers=[("a", "b")], http_version="1.0")
    # fields are normalized
    assert req.method == b"GET"
    assert req.target == b"/"
    assert req.headers == [(b"a", b"b")]
    assert req.http_version == b"1.0"

    # This is also okay -- has a Host (with weird capitalization, which is ok)
    req = Request(
        method="GET",
        target="/",
        headers=[("a", "b"), ("hOSt", "example.com")],
        http_version="1.1",
    )
    # we normalize header capitalization
    assert req.headers == [(b"a", b"b"), (b"host", b"example.com")]

    # Multiple host is bad too
    with pytest.raises(LocalProtocolError):
        req = Request(
            method="GET",
            target="/",
            headers=[("Host", "a"), ("Host", "a")],
            http_version="1.1",
        )
    # Even for HTTP/1.0
    with pytest.raises(LocalProtocolError):
        req = Request(
            method="GET",
            target="/",
            headers=[("Host", "a"), ("Host", "a")],
            http_version="1.0",
        )

    # Header values are validated
    for bad_char in "\x00\r\n\f\v":
        with pytest.raises(LocalProtocolError):
            req = Request(
                method="GET",
                target="/",
                headers=[("Host", "a"), ("Foo", "asd" + bad_char)],
                http_version="1.0",
            )

    # But for compatibility we allow non-whitespace control characters, even
    # though they're forbidden by the spec.
    Request(
        method="GET",
        target="/",
        headers=[("Host", "a"), ("Foo", "asd\x01\x02\x7f")],
        http_version="1.0",
    )

    # Request target is validated
    for bad_byte in b"\x00\x20\x7f\xee":
        target = bytearray(b"/")
        target.append(bad_byte)
        with pytest.raises(LocalProtocolError):
            Request(
                method="GET", target=target, headers=[("Host", "a")], http_version="1.1"
            )

    # Request method is validated
    with pytest.raises(LocalProtocolError):
        Request(
            method="GET / HTTP/1.1",
            target=target,
            headers=[("Host", "a")],
            http_version="1.1",
        )

    ir = InformationalResponse(status_code=100, headers=[("Host", "a")])
    assert ir.status_code == 100
    assert ir.headers == [(b"host", b"a")]
    assert ir.http_version == b"1.1"

    with pytest.raises(LocalProtocolError):
        InformationalResponse(status_code=200, headers=[("Host", "a")])

    resp = Response(status_code=204, headers=[], http_version="1.0")  # type: ignore[arg-type]
    assert resp.status_code == 204
    assert resp.headers == []
    assert resp.http_version == b"1.0"

    with pytest.raises(LocalProtocolError):
        resp = Response(status_code=100, headers=[], http_version="1.0")  # type: ignore[arg-type]

    with pytest.raises(LocalProtocolError):
        Response(status_code="100", headers=[], http_version="1.0")  # type: ignore[arg-type]

    with pytest.raises(LocalProtocolError):
        InformationalResponse(status_code=b"100", headers=[], http_version="1.0")  # type: ignore[arg-type]

    d = Data(data=b"asdf")
    assert d.data == b"asdf"

    eom = EndOfMessage()
    assert eom.headers == []

    cc = ConnectionClosed()
    assert repr(cc) == "ConnectionClosed()"


def test_intenum_status_code() -> None:
    # https://github.com/python-hyper/h11/issues/72

    r = Response(status_code=HTTPStatus.OK, headers=[], http_version="1.0")  # type: ignore[arg-type]
    assert r.status_code == HTTPStatus.OK
    assert type(r.status_code) is not type(HTTPStatus.OK)
    assert type(r.status_code) is int


def test_header_casing() -> None:
    r = Request(
        method="GET",
        target="/",
        headers=[("Host", "example.org"), ("Connection", "keep-alive")],
        http_version="1.1",
    )
    assert len(r.headers) == 2
    assert r.headers[0] == (b"host", b"example.org")
    assert r.headers == [(b"host", b"example.org"), (b"connection", b"keep-alive")]
    assert r.headers.raw_items() == [
        (b"Host", b"example.org"),
        (b"Connection", b"keep-alive"),
    ]
