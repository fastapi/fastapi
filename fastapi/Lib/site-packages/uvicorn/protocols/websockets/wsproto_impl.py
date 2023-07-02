import asyncio
import logging
import sys
import typing
from urllib.parse import unquote

import wsproto
from wsproto import ConnectionType, events
from wsproto.connection import ConnectionState
from wsproto.extensions import Extension, PerMessageDeflate
from wsproto.utilities import RemoteProtocolError

from uvicorn.config import Config
from uvicorn.logging import TRACE_LOG_LEVEL
from uvicorn.protocols.utils import (
    get_local_addr,
    get_path_with_query_string,
    get_remote_addr,
    is_ssl,
)
from uvicorn.server import ServerState

if typing.TYPE_CHECKING:
    from asgiref.typing import (
        ASGISendEvent,
        WebSocketAcceptEvent,
        WebSocketCloseEvent,
        WebSocketConnectEvent,
        WebSocketDisconnectEvent,
        WebSocketReceiveEvent,
        WebSocketScope,
        WebSocketSendEvent,
    )

    WebSocketEvent = typing.Union[
        "WebSocketReceiveEvent",
        "WebSocketDisconnectEvent",
        "WebSocketConnectEvent",
    ]

if sys.version_info < (3, 8):  # pragma: py-gte-38
    from typing_extensions import Literal
else:  # pragma: py-lt-38
    from typing import Literal


class WSProtocol(asyncio.Protocol):
    def __init__(
        self,
        config: Config,
        server_state: ServerState,
        app_state: typing.Dict[str, typing.Any],
        _loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        if not config.loaded:
            config.load()

        self.config = config
        self.app = config.loaded_app
        self.loop = _loop or asyncio.get_event_loop()
        self.logger = logging.getLogger("uvicorn.error")
        self.root_path = config.root_path
        self.app_state = app_state

        # Shared server state
        self.connections = server_state.connections
        self.tasks = server_state.tasks
        self.default_headers = server_state.default_headers

        # Connection state
        self.transport: asyncio.Transport = None  # type: ignore[assignment]
        self.server: typing.Optional[typing.Tuple[str, int]] = None
        self.client: typing.Optional[typing.Tuple[str, int]] = None
        self.scheme: Literal["wss", "ws"] = None  # type: ignore[assignment]

        # WebSocket state
        self.queue: asyncio.Queue["WebSocketEvent"] = asyncio.Queue()
        self.handshake_complete = False
        self.close_sent = False

        self.conn = wsproto.WSConnection(connection_type=ConnectionType.SERVER)

        self.read_paused = False
        self.writable = asyncio.Event()
        self.writable.set()

        # Buffers
        self.bytes = b""
        self.text = ""

    # Protocol interface

    def connection_made(  # type: ignore[override]
        self, transport: asyncio.Transport
    ) -> None:
        self.connections.add(self)
        self.transport = transport
        self.server = get_local_addr(transport)
        self.client = get_remote_addr(transport)
        self.scheme = "wss" if is_ssl(transport) else "ws"

        if self.logger.level <= TRACE_LOG_LEVEL:
            prefix = "%s:%d - " % self.client if self.client else ""
            self.logger.log(TRACE_LOG_LEVEL, "%sWebSocket connection made", prefix)

    def connection_lost(self, exc: typing.Optional[Exception]) -> None:
        code = 1005 if self.handshake_complete else 1006
        self.queue.put_nowait({"type": "websocket.disconnect", "code": code})
        self.connections.remove(self)

        if self.logger.level <= TRACE_LOG_LEVEL:
            prefix = "%s:%d - " % self.client if self.client else ""
            self.logger.log(TRACE_LOG_LEVEL, "%sWebSocket connection lost", prefix)

        self.handshake_complete = True
        if exc is None:
            self.transport.close()

    def eof_received(self) -> None:
        pass

    def data_received(self, data: bytes) -> None:
        try:
            self.conn.receive_data(data)
        except RemoteProtocolError as err:
            # TODO: Remove `type: ignore` when wsproto fixes the type annotation.
            self.transport.write(self.conn.send(err.event_hint))  # type: ignore[arg-type]  # noqa: E501
            self.transport.close()
        else:
            self.handle_events()

    def handle_events(self) -> None:
        for event in self.conn.events():
            if isinstance(event, events.Request):
                self.handle_connect(event)
            elif isinstance(event, events.TextMessage):
                self.handle_text(event)
            elif isinstance(event, events.BytesMessage):
                self.handle_bytes(event)
            elif isinstance(event, events.CloseConnection):
                self.handle_close(event)
            elif isinstance(event, events.Ping):
                self.handle_ping(event)

    def pause_writing(self) -> None:
        """
        Called by the transport when the write buffer exceeds the high water mark.
        """
        self.writable.clear()

    def resume_writing(self) -> None:
        """
        Called by the transport when the write buffer drops below the low water mark.
        """
        self.writable.set()

    def shutdown(self) -> None:
        if self.handshake_complete:
            self.queue.put_nowait({"type": "websocket.disconnect", "code": 1012})
            output = self.conn.send(wsproto.events.CloseConnection(code=1012))
            self.transport.write(output)
        else:
            self.send_500_response()
        self.transport.close()

    def on_task_complete(self, task: asyncio.Task) -> None:
        self.tasks.discard(task)

    # Event handlers

    def handle_connect(self, event: events.Request) -> None:
        headers = [(b"host", event.host.encode())]
        headers += [(key.lower(), value) for key, value in event.extra_headers]
        raw_path, _, query_string = event.target.partition("?")
        self.scope: "WebSocketScope" = {  # type: ignore[typeddict-item]
            "type": "websocket",
            "asgi": {"version": self.config.asgi_version, "spec_version": "2.3"},
            "http_version": "1.1",
            "scheme": self.scheme,
            "server": self.server,
            "client": self.client,
            "root_path": self.root_path,
            "path": unquote(raw_path),
            "raw_path": raw_path.encode("ascii"),
            "query_string": query_string.encode("ascii"),
            "headers": headers,
            "subprotocols": event.subprotocols,
            "extensions": None,
            "state": self.app_state.copy(),
        }
        self.queue.put_nowait({"type": "websocket.connect"})
        task = self.loop.create_task(self.run_asgi())
        task.add_done_callback(self.on_task_complete)
        self.tasks.add(task)

    def handle_text(self, event: events.TextMessage) -> None:
        self.text += event.data
        if event.message_finished:
            msg: "WebSocketReceiveEvent" = {  # type: ignore[typeddict-item]
                "type": "websocket.receive",
                "text": self.text,
            }
            self.queue.put_nowait(msg)
            self.text = ""
            if not self.read_paused:
                self.read_paused = True
                self.transport.pause_reading()

    def handle_bytes(self, event: events.BytesMessage) -> None:
        self.bytes += event.data
        # todo: we may want to guard the size of self.bytes and self.text
        if event.message_finished:
            msg: "WebSocketReceiveEvent" = {  # type: ignore[typeddict-item]
                "type": "websocket.receive",
                "bytes": self.bytes,
            }
            self.queue.put_nowait(msg)
            self.bytes = b""
            if not self.read_paused:
                self.read_paused = True
                self.transport.pause_reading()

    def handle_close(self, event: events.CloseConnection) -> None:
        if self.conn.state == ConnectionState.REMOTE_CLOSING:
            self.transport.write(self.conn.send(event.response()))
        self.queue.put_nowait({"type": "websocket.disconnect", "code": event.code})
        self.transport.close()

    def handle_ping(self, event: events.Ping) -> None:
        self.transport.write(self.conn.send(event.response()))

    def send_500_response(self) -> None:
        headers = [
            (b"content-type", b"text/plain; charset=utf-8"),
            (b"connection", b"close"),
        ]
        output = self.conn.send(
            wsproto.events.RejectConnection(
                status_code=500, headers=headers, has_body=True
            )
        )
        output += self.conn.send(
            wsproto.events.RejectData(data=b"Internal Server Error")
        )
        self.transport.write(output)

    async def run_asgi(self) -> None:
        try:
            result = await self.app(self.scope, self.receive, self.send)
        except BaseException:
            self.logger.exception("Exception in ASGI application\n")
            if not self.handshake_complete:
                self.send_500_response()
            self.transport.close()
        else:
            if not self.handshake_complete:
                msg = "ASGI callable returned without completing handshake."
                self.logger.error(msg)
                self.send_500_response()
                self.transport.close()
            elif result is not None:
                msg = "ASGI callable should return None, but returned '%s'."
                self.logger.error(msg, result)
                self.transport.close()

    async def send(self, message: "ASGISendEvent") -> None:
        await self.writable.wait()

        message_type = message["type"]

        if not self.handshake_complete:
            if message_type == "websocket.accept":
                message = typing.cast("WebSocketAcceptEvent", message)
                self.logger.info(
                    '%s - "WebSocket %s" [accepted]',
                    self.scope["client"],
                    get_path_with_query_string(self.scope),
                )
                subprotocol = message.get("subprotocol")
                extra_headers = self.default_headers + list(message.get("headers", []))
                extensions: typing.List[Extension] = []
                if self.config.ws_per_message_deflate:
                    extensions.append(PerMessageDeflate())
                if not self.transport.is_closing():
                    self.handshake_complete = True
                    output = self.conn.send(
                        wsproto.events.AcceptConnection(
                            subprotocol=subprotocol,
                            extensions=extensions,
                            extra_headers=extra_headers,
                        )
                    )
                    self.transport.write(output)

            elif message_type == "websocket.close":
                self.queue.put_nowait({"type": "websocket.disconnect", "code": 1006})
                self.logger.info(
                    '%s - "WebSocket %s" 403',
                    self.scope["client"],
                    get_path_with_query_string(self.scope),
                )
                self.handshake_complete = True
                self.close_sent = True
                event = events.RejectConnection(status_code=403, headers=[])
                output = self.conn.send(event)
                self.transport.write(output)
                self.transport.close()

            else:
                msg = (
                    "Expected ASGI message 'websocket.accept' or 'websocket.close', "
                    "but got '%s'."
                )
                raise RuntimeError(msg % message_type)

        elif not self.close_sent:
            if message_type == "websocket.send":
                message = typing.cast("WebSocketSendEvent", message)
                bytes_data = message.get("bytes")
                text_data = message.get("text")
                data = text_data if bytes_data is None else bytes_data
                output = self.conn.send(
                    wsproto.events.Message(data=data)  # type: ignore[type-var]
                )
                if not self.transport.is_closing():
                    self.transport.write(output)

            elif message_type == "websocket.close":
                message = typing.cast("WebSocketCloseEvent", message)
                self.close_sent = True
                code = message.get("code", 1000)
                reason = message.get("reason", "") or ""
                self.queue.put_nowait({"type": "websocket.disconnect", "code": code})
                output = self.conn.send(
                    wsproto.events.CloseConnection(code=code, reason=reason)
                )
                if not self.transport.is_closing():
                    self.transport.write(output)
                    self.transport.close()

            else:
                msg = (
                    "Expected ASGI message 'websocket.send' or 'websocket.close',"
                    " but got '%s'."
                )
                raise RuntimeError(msg % message_type)

        else:
            msg = "Unexpected ASGI message '%s', after sending 'websocket.close'."
            raise RuntimeError(msg % message_type)

    async def receive(self) -> "WebSocketEvent":
        message = await self.queue.get()
        if self.read_paused and self.queue.empty():
            self.read_paused = False
            self.transport.resume_reading()
        return message
