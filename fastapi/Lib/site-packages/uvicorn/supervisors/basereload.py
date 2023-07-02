import logging
import os
import signal
import sys
import threading
from pathlib import Path
from socket import socket
from types import FrameType
from typing import Callable, Iterator, List, Optional

import click

from uvicorn._subprocess import get_subprocess
from uvicorn.config import Config

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)

logger = logging.getLogger("uvicorn.error")


class BaseReload:
    def __init__(
        self,
        config: Config,
        target: Callable[[Optional[List[socket]]], None],
        sockets: List[socket],
    ) -> None:
        self.config = config
        self.target = target
        self.sockets = sockets
        self.should_exit = threading.Event()
        self.pid = os.getpid()
        self.is_restarting = False
        self.reloader_name: Optional[str] = None

    def signal_handler(self, sig: int, frame: Optional[FrameType]) -> None:
        """
        A signal handler that is registered with the parent process.
        """
        if sys.platform == "win32" and self.is_restarting:
            self.is_restarting = False  # pragma: py-not-win32
        else:
            self.should_exit.set()  # pragma: py-win32

    def run(self) -> None:
        self.startup()
        for changes in self:
            if changes:
                logger.warning(
                    "%s detected changes in %s. Reloading...",
                    self.reloader_name,
                    ", ".join(map(_display_path, changes)),
                )
                self.restart()

        self.shutdown()

    def pause(self) -> None:
        if self.should_exit.wait(self.config.reload_delay):
            raise StopIteration()

    def __iter__(self) -> Iterator[Optional[List[Path]]]:
        return self

    def __next__(self) -> Optional[List[Path]]:
        return self.should_restart()

    def startup(self) -> None:
        message = f"Started reloader process [{self.pid}] using {self.reloader_name}"
        color_message = "Started reloader process [{}] using {}".format(
            click.style(str(self.pid), fg="cyan", bold=True),
            click.style(str(self.reloader_name), fg="cyan", bold=True),
        )
        logger.info(message, extra={"color_message": color_message})

        for sig in HANDLED_SIGNALS:
            signal.signal(sig, self.signal_handler)

        self.process = get_subprocess(
            config=self.config, target=self.target, sockets=self.sockets
        )
        self.process.start()

    def restart(self) -> None:
        if sys.platform == "win32":  # pragma: py-not-win32
            self.is_restarting = True
            assert self.process.pid is not None
            os.kill(self.process.pid, signal.CTRL_C_EVENT)
        else:  # pragma: py-win32
            self.process.terminate()
        self.process.join()

        self.process = get_subprocess(
            config=self.config, target=self.target, sockets=self.sockets
        )
        self.process.start()

    def shutdown(self) -> None:
        if sys.platform == "win32":
            self.should_exit.set()  # pragma: py-not-win32
        else:
            self.process.terminate()  # pragma: py-win32
        self.process.join()

        for sock in self.sockets:
            sock.close()

        message = "Stopping reloader process [{}]".format(str(self.pid))
        color_message = "Stopping reloader process [{}]".format(
            click.style(str(self.pid), fg="cyan", bold=True)
        )
        logger.info(message, extra={"color_message": color_message})

    def should_restart(self) -> Optional[List[Path]]:
        raise NotImplementedError("Reload strategies should override should_restart()")


def _display_path(path: Path) -> str:
    try:
        return f"'{path.relative_to(Path.cwd())}'"
    except ValueError:
        return f"'{path}'"
