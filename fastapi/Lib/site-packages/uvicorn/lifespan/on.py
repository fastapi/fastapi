import asyncio
import logging
from asyncio import Queue
from typing import TYPE_CHECKING, Any, Dict, Union

from uvicorn import Config

if TYPE_CHECKING:
    from asgiref.typing import (
        LifespanScope,
        LifespanShutdownCompleteEvent,
        LifespanShutdownEvent,
        LifespanShutdownFailedEvent,
        LifespanStartupCompleteEvent,
        LifespanStartupEvent,
        LifespanStartupFailedEvent,
    )

    LifespanReceiveMessage = Union[LifespanStartupEvent, LifespanShutdownEvent]
    LifespanSendMessage = Union[
        LifespanStartupFailedEvent,
        LifespanShutdownFailedEvent,
        LifespanStartupCompleteEvent,
        LifespanShutdownCompleteEvent,
    ]


STATE_TRANSITION_ERROR = "Got invalid state transition on lifespan protocol."


class LifespanOn:
    def __init__(self, config: Config) -> None:
        if not config.loaded:
            config.load()

        self.config = config
        self.logger = logging.getLogger("uvicorn.error")
        self.startup_event = asyncio.Event()
        self.shutdown_event = asyncio.Event()
        self.receive_queue: "Queue[LifespanReceiveMessage]" = asyncio.Queue()
        self.error_occured = False
        self.startup_failed = False
        self.shutdown_failed = False
        self.should_exit = False
        self.state: Dict[str, Any] = {}

    async def startup(self) -> None:
        self.logger.info("Waiting for application startup.")

        loop = asyncio.get_event_loop()
        main_lifespan_task = loop.create_task(self.main())  # noqa: F841
        # Keep a hard reference to prevent garbage collection
        # See https://github.com/encode/uvicorn/pull/972
        startup_event: LifespanStartupEvent = {"type": "lifespan.startup"}
        await self.receive_queue.put(startup_event)
        await self.startup_event.wait()

        if self.startup_failed or (self.error_occured and self.config.lifespan == "on"):
            self.logger.error("Application startup failed. Exiting.")
            self.should_exit = True
        else:
            self.logger.info("Application startup complete.")

    async def shutdown(self) -> None:
        if self.error_occured:
            return
        self.logger.info("Waiting for application shutdown.")
        shutdown_event: LifespanShutdownEvent = {"type": "lifespan.shutdown"}
        await self.receive_queue.put(shutdown_event)
        await self.shutdown_event.wait()

        if self.shutdown_failed or (
            self.error_occured and self.config.lifespan == "on"
        ):
            self.logger.error("Application shutdown failed. Exiting.")
            self.should_exit = True
        else:
            self.logger.info("Application shutdown complete.")

    async def main(self) -> None:
        try:
            app = self.config.loaded_app
            scope: LifespanScope = {  # type: ignore[typeddict-item]
                "type": "lifespan",
                "asgi": {"version": self.config.asgi_version, "spec_version": "2.0"},
                "state": self.state,
            }
            await app(scope, self.receive, self.send)
        except BaseException as exc:
            self.asgi = None
            self.error_occured = True
            if self.startup_failed or self.shutdown_failed:
                return
            if self.config.lifespan == "auto":
                msg = "ASGI 'lifespan' protocol appears unsupported."
                self.logger.info(msg)
            else:
                msg = "Exception in 'lifespan' protocol\n"
                self.logger.error(msg, exc_info=exc)
        finally:
            self.startup_event.set()
            self.shutdown_event.set()

    async def send(self, message: "LifespanSendMessage") -> None:
        assert message["type"] in (
            "lifespan.startup.complete",
            "lifespan.startup.failed",
            "lifespan.shutdown.complete",
            "lifespan.shutdown.failed",
        )

        if message["type"] == "lifespan.startup.complete":
            assert not self.startup_event.is_set(), STATE_TRANSITION_ERROR
            assert not self.shutdown_event.is_set(), STATE_TRANSITION_ERROR
            self.startup_event.set()

        elif message["type"] == "lifespan.startup.failed":
            assert not self.startup_event.is_set(), STATE_TRANSITION_ERROR
            assert not self.shutdown_event.is_set(), STATE_TRANSITION_ERROR
            self.startup_event.set()
            self.startup_failed = True
            if message.get("message"):
                self.logger.error(message["message"])

        elif message["type"] == "lifespan.shutdown.complete":
            assert self.startup_event.is_set(), STATE_TRANSITION_ERROR
            assert not self.shutdown_event.is_set(), STATE_TRANSITION_ERROR
            self.shutdown_event.set()

        elif message["type"] == "lifespan.shutdown.failed":
            assert self.startup_event.is_set(), STATE_TRANSITION_ERROR
            assert not self.shutdown_event.is_set(), STATE_TRANSITION_ERROR
            self.shutdown_event.set()
            self.shutdown_failed = True
            if message.get("message"):
                self.logger.error(message["message"])

    async def receive(self) -> "LifespanReceiveMessage":
        return await self.receive_queue.get()
