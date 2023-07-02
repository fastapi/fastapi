import logging
from pathlib import Path
from socket import socket
from typing import Callable, Dict, Iterator, List, Optional

from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

logger = logging.getLogger("uvicorn.error")


class StatReload(BaseReload):
    def __init__(
        self,
        config: Config,
        target: Callable[[Optional[List[socket]]], None],
        sockets: List[socket],
    ) -> None:
        super().__init__(config, target, sockets)
        self.reloader_name = "StatReload"
        self.mtimes: Dict[Path, float] = {}

        if config.reload_excludes or config.reload_includes:
            logger.warning(
                "--reload-include and --reload-exclude have no effect unless "
                "watchfiles is installed."
            )

    def should_restart(self) -> Optional[List[Path]]:
        self.pause()

        for file in self.iter_py_files():
            try:
                mtime = file.stat().st_mtime
            except OSError:  # pragma: nocover
                continue

            old_time = self.mtimes.get(file)
            if old_time is None:
                self.mtimes[file] = mtime
                continue
            elif mtime > old_time:
                return [file]
        return None

    def restart(self) -> None:
        self.mtimes = {}
        return super().restart()

    def iter_py_files(self) -> Iterator[Path]:
        for reload_dir in self.config.reload_dirs:
            for path in list(reload_dir.rglob("*.py")):
                yield path.resolve()
