import logging
import warnings
from pathlib import Path
from socket import socket
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from watchgod import DefaultWatcher

from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

if TYPE_CHECKING:
    import os

    DirEntry = os.DirEntry[str]

logger = logging.getLogger("uvicorn.error")


class CustomWatcher(DefaultWatcher):
    def __init__(self, root_path: Path, config: Config):
        default_includes = ["*.py"]
        self.includes = [
            default
            for default in default_includes
            if default not in config.reload_excludes
        ]
        self.includes.extend(config.reload_includes)
        self.includes = list(set(self.includes))

        default_excludes = [".*", ".py[cod]", ".sw.*", "~*"]
        self.excludes = [
            default
            for default in default_excludes
            if default not in config.reload_includes
        ]
        self.excludes.extend(config.reload_excludes)
        self.excludes = list(set(self.excludes))

        self.watched_dirs: Dict[str, bool] = {}
        self.watched_files: Dict[str, bool] = {}
        self.dirs_includes = set(config.reload_dirs)
        self.dirs_excludes = set(config.reload_dirs_excludes)
        self.resolved_root = root_path
        super().__init__(str(root_path))

    def should_watch_file(self, entry: "DirEntry") -> bool:
        cached_result = self.watched_files.get(entry.path)
        if cached_result is not None:
            return cached_result

        entry_path = Path(entry)

        # cwd is not verified through should_watch_dir, so we need to verify here
        if entry_path.parent == Path.cwd() and Path.cwd() not in self.dirs_includes:
            self.watched_files[entry.path] = False
            return False
        for include_pattern in self.includes:
            if entry_path.match(include_pattern):
                for exclude_pattern in self.excludes:
                    if entry_path.match(exclude_pattern):
                        self.watched_files[entry.path] = False
                        return False
                self.watched_files[entry.path] = True
                return True
        self.watched_files[entry.path] = False
        return False

    def should_watch_dir(self, entry: "DirEntry") -> bool:
        cached_result = self.watched_dirs.get(entry.path)
        if cached_result is not None:
            return cached_result

        entry_path = Path(entry)

        if entry_path in self.dirs_excludes:
            self.watched_dirs[entry.path] = False
            return False

        for exclude_pattern in self.excludes:
            if entry_path.match(exclude_pattern):
                is_watched = False
                if entry_path in self.dirs_includes:
                    is_watched = True

                for directory in self.dirs_includes:
                    if directory in entry_path.parents:
                        is_watched = True

                if is_watched:
                    logger.debug(
                        "WatchGodReload detected a new excluded dir '%s' in '%s'; "
                        "Adding to exclude list.",
                        entry_path.relative_to(self.resolved_root),
                        str(self.resolved_root),
                    )
                self.watched_dirs[entry.path] = False
                self.dirs_excludes.add(entry_path)
                return False

        if entry_path in self.dirs_includes:
            self.watched_dirs[entry.path] = True
            return True

        for directory in self.dirs_includes:
            if directory in entry_path.parents:
                self.watched_dirs[entry.path] = True
                return True

        for include_pattern in self.includes:
            if entry_path.match(include_pattern):
                logger.info(
                    "WatchGodReload detected a new reload dir '%s' in '%s'; "
                    "Adding to watch list.",
                    str(entry_path.relative_to(self.resolved_root)),
                    str(self.resolved_root),
                )
                self.dirs_includes.add(entry_path)
                self.watched_dirs[entry.path] = True
                return True

        self.watched_dirs[entry.path] = False
        return False


class WatchGodReload(BaseReload):
    def __init__(
        self,
        config: Config,
        target: Callable[[Optional[List[socket]]], None],
        sockets: List[socket],
    ) -> None:
        warnings.warn(
            '"watchgod" is deprecated, you should switch '
            "to watchfiles (`pip install watchfiles`).",
            DeprecationWarning,
        )
        super().__init__(config, target, sockets)
        self.reloader_name = "WatchGod"
        self.watchers = []
        reload_dirs = []
        for directory in config.reload_dirs:
            if Path.cwd() not in directory.parents:
                reload_dirs.append(directory)
        if Path.cwd() not in reload_dirs:
            reload_dirs.append(Path.cwd())
        for w in reload_dirs:
            self.watchers.append(CustomWatcher(w.resolve(), self.config))

    def should_restart(self) -> Optional[List[Path]]:
        self.pause()

        for watcher in self.watchers:
            change = watcher.check()
            if change != set():
                return list({Path(c[1]) for c in change})

        return None
