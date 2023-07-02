import asyncio
import typing

if typing.TYPE_CHECKING:
    from asgiref.typing import (
        ASGIReceiveCallable,
        ASGISendCallable,
        HTTPResponseBodyEvent,
        HTTPResponseStartEvent,
        Scope,
    )

CLOSE_HEADER = (b"connection", b"close")

HIGH_WATER_LIMIT = 65536


class FlowControl:
    def __init__(self, transport: asyncio.Transport) -> None:
        self._transport = transport
        self.read_paused = False
        self.write_paused = False
        self._is_writable_event = asyncio.Event()
        self._is_writable_event.set()

    async def drain(self) -> None:
        await self._is_writable_event.wait()

    def pause_reading(self) -> None:
        if not self.read_paused:
            self.read_paused = True
            self._transport.pause_reading()

    def resume_reading(self) -> None:
        if self.read_paused:
            self.read_paused = False
            self._transport.resume_reading()

    def pause_writing(self) -> None:
        if not self.write_paused:
            self.write_paused = True
            self._is_writable_event.clear()

    def resume_writing(self) -> None:
        if self.write_paused:
            self.write_paused = False
            self._is_writable_event.set()


async def service_unavailable(
    scope: "Scope", receive: "ASGIReceiveCallable", send: "ASGISendCallable"
) -> None:
    response_start: "HTTPResponseStartEvent" = {
        "type": "http.response.start",
        "status": 503,
        "headers": [
            (b"content-type", b"text/plain; charset=utf-8"),
            (b"connection", b"close"),
        ],
    }
    await send(response_start)

    response_body: "HTTPResponseBodyEvent" = {
        "type": "http.response.body",
        "body": b"Service Unavailable",
        "more_body": False,
    }
    await send(response_body)
