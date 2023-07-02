from __future__ import annotations

import logging
import os
import re
import zipfile
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser
from itertools import chain
from pathlib import Path
from tempfile import mkdtemp

from distlib.scripts import ScriptMaker, enquote_executable

from virtualenv.util.path import safe_delete


class PipInstall(metaclass=ABCMeta):
    def __init__(self, wheel, creator, image_folder) -> None:
        self._wheel = wheel
        self._creator = creator
        self._image_dir = image_folder
        self._extracted = False
        self.__dist_info = None
        self._console_entry_points = None

    @abstractmethod
    def _sync(self, src, dst):
        raise NotImplementedError

    def install(self, version_info):
        self._extracted = True
        self._uninstall_previous_version()
        # sync image
        for filename in self._image_dir.iterdir():
            into = self._creator.purelib / filename.name
            self._sync(filename, into)
        # generate console executables
        consoles = set()
        script_dir = self._creator.script_dir
        for name, module in self._console_scripts.items():
            consoles.update(
                self._create_console_entry_point(name, module, script_dir, version_info)
            )
        logging.debug(
            "generated console scripts %s", " ".join(i.name for i in consoles)
        )

    def build_image(self):
        # 1. first extract the wheel
        logging.debug(
            "build install image for %s to %s", self._wheel.name, self._image_dir
        )
        with zipfile.ZipFile(str(self._wheel)) as zip_ref:
            self._shorten_path_if_needed(zip_ref)
            zip_ref.extractall(str(self._image_dir))
            self._extracted = True
        # 2. now add additional files not present in the distribution
        new_files = self._generate_new_files()
        # 3. finally fix the records file
        self._fix_records(new_files)

    def _shorten_path_if_needed(self, zip_ref):
        if os.name == "nt":
            to_folder = str(self._image_dir)
            # https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation
            zip_max_len = max(len(i) for i in zip_ref.namelist())
            path_len = zip_max_len + len(to_folder)
            if path_len > 260:  # noqa: PLR2004
                self._image_dir.mkdir(exist_ok=True)  # to get a short path must exist

                from virtualenv.util.path import get_short_path_name

                to_folder = get_short_path_name(to_folder)
                self._image_dir = Path(to_folder)

    def _records_text(self, files):
        return "\n".join(
            f"{os.path.relpath(str(rec), str(self._image_dir))},," for rec in files
        )

    def _generate_new_files(self):
        new_files = set()
        installer = self._dist_info / "INSTALLER"
        installer.write_text("pip\n", encoding="utf-8")
        new_files.add(installer)
        # inject a no-op root element, as workaround for bug in https://github.com/pypa/pip/issues/7226
        marker = self._image_dir / f"{self._dist_info.stem}.virtualenv"
        marker.write_text("", encoding="utf-8")
        new_files.add(marker)
        folder = mkdtemp()
        try:
            to_folder = Path(folder)
            rel = os.path.relpath(
                str(self._creator.script_dir), str(self._creator.purelib)
            )
            version_info = self._creator.interpreter.version_info
            for name, module in self._console_scripts.items():
                new_files.update(
                    Path(os.path.normpath(str(self._image_dir / rel / i.name)))
                    for i in self._create_console_entry_point(
                        name, module, to_folder, version_info
                    )
                )
        finally:
            safe_delete(folder)
        return new_files

    @property
    def _dist_info(self):
        if self._extracted is False:
            return None  # pragma: no cover
        if self.__dist_info is None:
            files = []
            for filename in self._image_dir.iterdir():
                files.append(filename.name)
                if filename.suffix == ".dist-info":
                    self.__dist_info = filename
                    break
            else:
                msg = f"no .dist-info at {self._image_dir}, has {', '.join(files)}"
                raise RuntimeError(msg)  # pragma: no cover
        return self.__dist_info

    @abstractmethod
    def _fix_records(self, extra_record_data):
        raise NotImplementedError

    @property
    def _console_scripts(self):
        if self._extracted is False:
            return None  # pragma: no cover
        if self._console_entry_points is None:
            self._console_entry_points = {}
            entry_points = self._dist_info / "entry_points.txt"
            if entry_points.exists():
                parser = ConfigParser()
                with entry_points.open(encoding="utf-8") as file_handler:
                    parser.read_file(file_handler)
                if "console_scripts" in parser.sections():
                    for name, value in parser.items("console_scripts"):
                        match = re.match(r"(.*?)-?\d\.?\d*", name)
                        our_name = match.groups(1)[0] if match else name
                        self._console_entry_points[our_name] = value
        return self._console_entry_points

    def _create_console_entry_point(self, name, value, to_folder, version_info):
        result = []
        maker = ScriptMakerCustom(to_folder, version_info, self._creator.exe, name)
        specification = f"{name} = {value}"
        new_files = maker.make(specification)
        result.extend(Path(i) for i in new_files)
        return result

    def _uninstall_previous_version(self):
        dist_name = self._dist_info.stem.split("-")[0]
        in_folders = chain.from_iterable(
            [i.iterdir() for i in (self._creator.purelib, self._creator.platlib)]
        )
        paths = (
            p
            for p in in_folders
            if p.stem.split("-")[0] == dist_name
            and p.suffix == ".dist-info"
            and p.is_dir()
        )
        existing_dist = next(paths, None)
        if existing_dist is not None:
            self._uninstall_dist(existing_dist)

    @staticmethod
    def _uninstall_dist(dist):
        dist_base = dist.parent
        logging.debug(
            "uninstall existing distribution %s from %s", dist.stem, dist_base
        )

        top_txt = dist / "top_level.txt"  # add top level packages at folder level
        paths = (
            {
                dist.parent / i.strip()
                for i in top_txt.read_text(encoding="utf-8").splitlines()
            }
            if top_txt.exists()
            else set()
        )
        paths.add(dist)  # add the dist-info folder itself

        base_dirs, record = (
            paths.copy(),
            dist / "RECORD",
        )  # collect entries in record that we did not register yet
        for name in (
            (i.split(",")[0] for i in record.read_text(encoding="utf-8").splitlines())
            if record.exists()
            else ()
        ):
            path = dist_base / name
            if not any(
                p in base_dirs for p in path.parents
            ):  # only add if not already added as a base dir
                paths.add(path)

        for path in sorted(paths):  # actually remove stuff in a stable order
            if path.exists():
                if path.is_dir() and not path.is_symlink():
                    safe_delete(path)
                else:
                    path.unlink()

    def clear(self):
        if self._image_dir.exists():
            safe_delete(self._image_dir)

    def has_image(self):
        return self._image_dir.exists() and next(self._image_dir.iterdir()) is not None


class ScriptMakerCustom(ScriptMaker):
    def __init__(self, target_dir, version_info, executable, name) -> None:
        super().__init__(None, str(target_dir))
        self.clobber = True  # overwrite
        self.set_mode = True  # ensure they are executable
        self.executable = enquote_executable(str(executable))
        self.version_info = version_info.major, version_info.minor
        self.variants = {"", "X", "X.Y"}
        self._name = name

    def _write_script(
        self, names, shebang, script_bytes, filenames, ext
    ):  # noqa: PLR0913
        names.add(f"{self._name}{self.version_info[0]}.{self.version_info[1]}")
        super()._write_script(names, shebang, script_bytes, filenames, ext)


__all__ = [
    "PipInstall",
]
