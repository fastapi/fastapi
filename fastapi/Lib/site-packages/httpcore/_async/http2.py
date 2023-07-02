import enum
import logging
import time
import types
import typing

import h2.config
import h2.connection
import h2.events
import h2.exceptions
import h2.settings

from .._exceptions import (
    ConnectionNotAvailable,
    LocalProtocolError,
    RemoteProtocolError,
)
from .._models import Origin, Request, Response
from .._synchronization import AsyncLock, AsyncSemaphore
from .._trace import Trace
from ..backends.base import AsyncNetworkStream
from .interfaces import AsyncConnectionInterface

logger = logging.getLogger("httpcore.http2")


def has_body_headers(request: Request) -> bool:
    return any(
        k.lower() == b"content-length" or k.lower() == b"transfer-encoding"
        for k, v in request.headers
    )


class HTTPConnectionState(enum.IntEnum):
    ACTIVE = 1
    IDLE = 2
    CLOSED = 3


class AsyncHTTP2Connection(AsyncConnectionInterface):
    READ_NUM_BYTES = 64 * 1024
    CONFIG = h2.config.H2Configuration(validate_inbound_headers=False)

    def __init__(
        self,
        origin: Origin,
        stream: AsyncNetworkStream,
        keepalive_expiry: typing.Optional[float] = None,
    ):
        self._origin = origin
        self._network_stream = stream
        self._keepalive_expiry: typing.Optional[float] = keepalive_expiry
        self._h2_state = h2.connection.H2Connection(config=self.CONFIG)
        self._state = HTTPConnectionState.IDLE
        self._expire_at: typing.Optional[float] = None
        self._request_count = 0
        self._init_lock = AsyncLock()
        self._state_lock = AsyncLock()
        self._read_lock = AsyncLock()
        self._write_lock = AsyncLock()
        self._sent_connection_init = False
        self._used_all_stream_ids = False
        self._connection_error = False
        self._events: typing.Dict[int, h2.events.Event] = {}
        self._read_exception: typing.Optional[Exception] = None
        self._write_exception: typing.Optional[Exception] = None
        self._connection_error_event: typing.Optional[h2.events.Event] = None

    async def handle_async_request(self, request: Request) -> Response:
        if not self.can_handle_request(request.url.origin):
            # This cannot occur in normal operation, since the connection pool
            # will only send requests on connections that handle them.
            # It's in place simply for resilience as a guard against incorrect
            # usage, for anyone working directly with httpcore connections.
            raise RuntimeError(
                f"Attempted to send request to {request.url.origin} on connection "
                f"to {self._origin}"
            )

        async with self._state_lock:
            if self._state in (HTTPConnectionState.ACTIVE, HTTPConnectionState.IDLE):
                self._request_count += 1
                self._expire_at = None
                self._state = HTTPConnectionState.ACTIVE
            else:
                raise ConnectionNotAvailable()

        async with self._init_lock:
            if not self._sent_connection_init:
                kwargs = {"request": request}
                async with Trace("send_connection_init", logger, request, kwargs):
                    await self._send_connection_init(**kwargs)
                self._sent_connection_init = True

                # Initially start with just 1 until the remote server provides
                # its max_concurrent_streams value
                self._max_streams = 1

                local_settings_max_streams = (
                    self._h2_state.local_settings.max_concurrent_streams
                )
                self._max_streams_semaphore = AsyncSemaphore(local_settings_max_streams)

                for _ in range(local_settings_max_streams - self._max_streams):
                    await self._max_streams_semaphore.acquire()

        await self._max_streams_semaphore.acquire()

        try:
            stream_id = self._h2_state.get_next_available_stream_id()
            self._events[stream_id] = []
        except h2.exceptions.NoAvailableStreamIDError:  # pragma: nocover
            self._used_all_stream_ids = True
            raise ConnectionNotAvailable()

        try:
            kwargs = {"request": request, "stream_id": stream_id}
            async with Trace("send_request_headers", logger, request, kwargs):
                await self._send_request_headers(request=request, stream_id=stream_id)
            async with Trace("send_request_body", logger, request, kwargs):
                await self._send_request_body(request=request, stream_id=stream_id)
            async with Trace(
                "receive_response_headers", logger, request, kwargs
            ) as trace:
                status, headers = await self._receive_response(
                    request=request, stream_id=stream_id
                )
                trace.return_value = (status, headers)

            return Response(
                status=status,
                headers=headers,
                content=HTTP2ConnectionByteStream(self, request, stream_id=stream_id),
                extensions={"stream_id": stream_id, "http_version": b"HTTP/2"},
            )
        except Exception as exc:  # noqa: PIE786
            kwargs = {"stream_id": stream_id}
            async with Trace("response_closed", logger, request, kwargs):
                await self._response_closed(stream_id=stream_id)

            if isinstance(exc, h2.exceptions.ProtocolError):
                # One case where h2 can raise a protocol error is when a
                # closed frame has been seen by the state machine.
                #
                # This happens when one stream is reading, and encounters
                # a GOAWAY event. Other flows of control may then raise
                # a protocol error at any point they interact with the 'h2_state'.
                #
                # In this case we'll have stored the event, and should raise
                # it as a RemoteProtocolError.
                if self._connection_error_event:
                    raise RemoteProtocolError(self._connection_error_event)
                # If h2 raises a protocol error in some other state then we
                # must somehow have made a protocol violation.
                raise LocalProtocolError(exc)  # pragma: nocover

            raise exc

    async def _send_connection_init(self, request: Request) -> None:
        """
        The HTTP/2 connection requires some initial setup before we can start
        using individual request/response streams on it.
        """
        # Need to set these manually here instead of manipulating via
        # __setitem__() otherwise the H2Connection will emit SettingsUpdate
        # frames in addition to sending the undesired defaults.
        self._h2_state.local_settings = h2.settings.Settings(
            client=True,
            initial_values={
                # Disable PUSH_PROMISE frames from the server since we don't do anything
                # with them for now.  Maybe when we support caching?
                h2.settings.SettingCodes.ENABLE_PUSH: 0,
                # These two are taken from h2 for safe defaults
                h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS: 100,
                h2.settings.SettingCodes.MAX_HEADER_LIST_SIZE: 65536,
            },
        )

        # Some websites (*cough* Yahoo *cough*) balk at this setting being
        # present in the initial handshake since it's not defined in the original
        # RFC despite the RFC mandating ignoring settings you don't know about.
        del self._h2_state.local_settings[
            h2.settings.SettingCodes.ENABLE_CONNECT_PROTOCOL
        ]

        self._h2_state.initiate_connection()
        self._h2_state.increment_flow_control_window(2**24)
        await self._write_outgoing_data(request)

    # Sending the request...

    async def _send_request_headers(self, request: Request, stream_id: int) -> None:
        end_stream = not has_body_headers(request)

        # In HTTP/2 the ':authority' pseudo-header is used instead of 'Host'.
        # In order to gracefully handle HTTP/1.1 and HTTP/2 we always require
        # HTTP/1.1 style headers, and map them appropriately if we end up on
        # an HTTP/2 connection.
        authority = [v for k, v in request.headers if k.lower() == b"host"][0]

        headers = [
            (b":method", request.method),
            (b":authority", authority),
            (b":scheme", request.url.scheme),
            (b":path", request.url.target),
        ] + [
            (k.lower(), v)
            for k, v in request.headers
            if k.lower()
            not in (
                b"host",
                b"transfer-encoding",
            )
        ]

        self._h2_state.send_headers(stream_id, headers, end_stream=end_stream)
        self._h2_state.increment_flow_control_window(2**24, stream_id=stream_id)
        await self._write_outgoing_data(request)

    async def _send_request_body(self, request: Request, stream_id: int) -> None:
        if not has_body_headers(request):
            return

        assert isinstance(request.stream, typing.AsyncIterable)
        async for data in request.stream:
            while data:
                max_flow = await self._wait_for_outgoing_flow(request, stream_id)
                chunk_size = min(len(data), max_flow)
                chunk, data = data[:chunk_size], data[chunk_size:]
                self._h2_state.send_data(stream_id, chunk)
                await self._write_outgoing_data(request)

        self._h2_state.end_stream(stream_id)
        await self._write_outgoing_data(request)

    # Receiving the response...

    async def _receive_response(
        self, request: Request, stream_id: int
    ) -> typing.Tuple[int, typing.List[typing.Tuple[bytes, bytes]]]:
        while True:
            event = await self._receive_stream_event(request, stream_id)
            if isinstance(event, h2.events.ResponseReceived):
                break

        status_code = 200
        headers = []
        for k, v in event.headers:
            if k == b":status":
                status_code = int(v.decode("ascii", errors="ignore"))
            elif not k.startswith(b":"):
                headers.append((k, v))

        return (status_code, headers)

    async def _receive_response_body(
        self, request: Request, stream_id: int
    ) -> typing.AsyncIterator[bytes]:
        while True:
            event = await self._receive_stream_event(request, stream_id)
            if isinstance(event, h2.events.DataReceived):
                amount = event.flow_controlled_length
                self._h2_state.acknowledge_received_data(amount, stream_id)
                await self._write_outgoing_data(request)
                yield event.data
            elif isinstance(event, (h2.events.StreamEnded, h2.events.StreamReset)):
                break

    async def _receive_stream_event(
        self, request: Request, stream_id: int
    ) -> h2.events.Event:
        while not self._events.get(stream_id):
            await self._receive_events(request, stream_id)
        event = self._events[stream_id].pop(0)
        # The StreamReset event applies to a single stream.
        if hasattr(event, "error_code"):
            raise RemoteProtocolError(event)
        return event

    async def _receive_events(
        self, request: Request, stream_id: typing.Optional[int] = None
    ) -> None:
        async with self._read_lock:
            if self._connection_error_event is not None:  # pragma: nocover
                raise RemoteProtocolError(self._connection_error_event)

            # This conditional is a bit icky. We don't want to block reading if we've
            # actually got an event to return for a given stream. We need to do that
            # check *within* the atomic read lock. Though it also need to be optional,
            # because when we call it from `_wait_for_outgoing_flow` we *do* want to
            # block until we've available flow control, event when we have events
            # pending for the stream ID we're attempting to send on.
            if stream_id is None or not self._events.get(stream_id):
                events = await self._read_incoming_data(request)
                for event in events:
                    if isinstance(event, h2.events.RemoteSettingsChanged):
                        async with Trace(
                            "receive_remote_settings", logger, request
                        ) as trace:
                            await self._receive_remote_settings_change(event)
                            trace.return_value = event

                    event_stream_id = getattr(event, "stream_id", 0)

                    # The ConnectionTerminatedEvent applies to the entire connection,
                    # and should be saved so it can be raised on all streams.
                    if hasattr(event, "error_code") and event_stream_id == 0:
                        self._connection_error_event = event
                        raise RemoteProtocolError(event)

                    if event_stream_id in self._events:
                        self._events[event_stream_id].append(event)

        await self._write_outgoing_data(request)

    async def _receive_remote_settings_change(self, event: h2.events.Event) -> None:
        max_concurrent_streams = event.changed_settings.get(
            h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS
        )
        if max_concurrent_streams:
            new_max_streams = min(
                max_concurrent_streams.new_value,
                self._h2_state.local_settings.max_concurrent_streams,
            )
            if new_max_streams and new_max_streams != self._max_streams:
                while new_max_streams > self._max_streams:
                    await self._max_streams_semaphore.release()
                    self._max_streams += 1
                while new_max_streams < self._max_streams:
                    await self._max_streams_semaphore.acquire()
                    self._max_streams -= 1

    async def _response_closed(self, stream_id: int) -> None:
        await self._max_streams_semaphore.release()
        del self._events[stream_id]
        async with self._state_lock:
            if self._state == HTTPConnectionState.ACTIVE and not self._events:
                self._state = HTTPConnectionState.IDLE
                if self._keepalive_expiry is not None:
                    now = time.monotonic()
                    self._expire_at = now + self._keepalive_expiry
                if self._used_all_stream_ids:  # pragma: nocover
                    await self.aclose()

    async def aclose(self) -> None:
        # Note that this method unilaterally closes the connection, and does
        # not have any kind of locking in place around it.
        self._h2_state.close_connection()
        self._state = HTTPConnectionState.CLOSED
        await self._network_stream.aclose()

    # Wrappers around network read/write operations...

    async def _read_incoming_data(
        self, request: Request
    ) -> typing.List[h2.events.Event]:
        timeouts = request.extensions.get("timeout", {})
        timeout = timeouts.get("read", None)

        if self._read_exception is not None:
            raise self._read_exception  # pragma: nocover

        try:
            data = await self._network_stream.read(self.READ_NUM_BYTES, timeout)
            if data == b"":
                raise RemoteProtocolError("Server disconnected")
        except Exception as exc:
            # If we get a network error we should:
            #
            # 1. Save the exception and just raise it immediately on any future reads.
            #    (For example, this means that a single read timeout or disconnect will
            #    immediately close all pending streams. Without requiring multiple
            #    sequential timeouts.)
            # 2. Mark the connection as errored, so that we don't accept any other
            #    incoming requests.
            self._read_exception = exc
            self._connection_error = True
            raise exc

        events: typing.List[h2.events.Event] = self._h2_state.receive_data(data)

        return events

    async def _write_outgoing_data(self, request: Request) -> None:
        timeouts = request.extensions.get("timeout", {})
        timeout = timeouts.get("write", None)

        async with self._write_lock:
            data_to_send = self._h2_state.data_to_send()

            if self._write_exception is not None:
                raise self._write_exception  # pragma: nocover

            try:
                await self._network_stream.write(data_to_send, timeout)
            except Exception as exc:  # pragma: nocover
                # If we get a network error we should:
                #
                # 1. Save the exception and just raise it immediately on any future write.
                #    (For example, this means that a single write timeout or disconnect will
                #    immediately close all pending streams. Without requiring multiple
                #    sequential timeouts.)
                # 2. Mark the connection as errored, so that we don't accept any other
                #    incoming requests.
                self._write_exception = exc
                self._connection_error = True
                raise exc

    # Flow control...

    async def _wait_for_outgoing_flow(self, request: Request, stream_id: int) -> int:
        """
        Returns the maximum allowable outgoing flow for a given stream.

        If the allowable flow is zero, then waits on the network until
        WindowUpdated frames have increased the flow rate.
        https://tools.ietf.org/html/rfc7540#section-6.9
        """
        local_flow: int = self._h2_state.local_flow_control_window(stream_id)
        max_frame_size: int = self._h2_state.max_outbound_frame_size
        flow = min(local_flow, max_frame_size)
        while flow == 0:
            await self._receive_events(request)
            local_flow = self._h2_state.local_flow_control_window(stream_id)
            max_frame_size = self._h2_state.max_outbound_frame_size
            flow = min(local_flow, max_frame_size)
        return flow

    # Interface for connection pooling...

    def can_handle_request(self, origin: Origin) -> bool:
        return origin == self._origin

    def is_available(self) -> bool:
        return (
            self._state != HTTPConnectionState.CLOSED
            and not self._connection_error
            and not self._used_all_stream_ids
            and not (
                self._h2_state.state_machine.state
                == h2.connection.ConnectionState.CLOSED
            )
        )

    def has_expired(self) -> bool:
        now = time.monotonic()
        return self._expire_at is not None and now > self._expire_at

    def is_idle(self) -> bool:
        return self._state == HTTPConnectionState.IDLE

    def is_closed(self) -> bool:
        return self._state == HTTPConnectionState.CLOSED

    def info(self) -> str:
        origin = str(self._origin)
        return (
            f"{origin!r}, HTTP/2, {self._state.name}, "
            f"Request Count: {self._request_count}"
        )

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        origin = str(self._origin)
        return (
            f"<{class_name} [{origin!r}, {self._state.name}, "
            f"Request Count: {self._request_count}]>"
        )

    # These context managers are not used in the standard flow, but are
    # useful for testing or working with connection instances directly.

    async def __aenter__(self) -> "AsyncHTTP2Connection":
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_value: typing.Optional[BaseException] = None,
        traceback: typing.Optional[types.TracebackType] = None,
    ) -> None:
        await self.aclose()


class HTTP2ConnectionByteStream:
    def __init__(
        self, connection: AsyncHTTP2Connection, request: Request, stream_id: int
    ) -> None:
        self._connection = connection
        self._request = request
        self._stream_id = stream_id
        self._closed = False

    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        kwargs = {"request": self._request, "stream_id": self._stream_id}
        try:
            async with Trace("receive_response_body", logger, self._request, kwargs):
                async for chunk in self._connection._receive_response_body(
                    request=self._request, stream_id=self._stream_id
                ):
                    yield chunk
        except BaseException as exc:
            # If we get an exception while streaming the response,
            # we want to close the response (and possibly the connection)
            # before raising that exception.
            await self.aclose()
            raise exc

    async def aclose(self) -> None:
        if not self._closed:
            self._closed = True
            kwargs = {"stream_id": self._stream_id}
            async with Trace("response_closed", logger, self._request, kwargs):
                await self._connection._response_closed(stream_id=self._stream_id)
