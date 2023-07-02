"""Bootstrap."""

from __future__ import annotations

import logging
import sys
import traceback
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError
from threading import Lock, Thread

from virtualenv.info import fs_supports_symlink
from virtualenv.seed.embed.base_embed import BaseEmbed
from virtualenv.seed.wheels import get_wheel

from .pip_install.copy import CopyPipInstall
from .pip_install.symlink import SymlinkPipInstall


class FromAppData(BaseEmbed):
    def __init__(self, options) -> None:
        super().__init__(options)
        self.symlinks = options.symlink_app_data

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, app_data):
        super().add_parser_arguments(parser, interpreter, app_data)
        can_symlink = app_data.transient is False and fs_supports_symlink()
        sym = "" if can_symlink else "not supported - "
        parser.add_argument(
            "--symlink-app-data",
            dest="symlink_app_data",
            action="store_true" if can_symlink else "store_false",
            help=f"{sym} symlink the python packages from the app-data folder (requires seed pip>=19.3)",
            default=False,
        )

    def run(self, creator):
        if not self.enabled:
            return
        with self._get_seed_wheels(creator) as name_to_whl:
            pip_version = (
                name_to_whl["pip"].version_tuple if "pip" in name_to_whl else None
            )
            installer_class = self.installer_class(pip_version)
            exceptions = {}

            def _install(name, wheel):
                try:
                    logging.debug(
                        "install %s from wheel %s via %s",
                        name,
                        wheel,
                        installer_class.__name__,
                    )
                    key = Path(installer_class.__name__) / wheel.path.stem
                    wheel_img = self.app_data.wheel_image(
                        creator.interpreter.version_release_str, key
                    )
                    installer = installer_class(wheel.path, creator, wheel_img)
                    parent = self.app_data.lock / wheel_img.parent
                    with parent.non_reentrant_lock_for_key(wheel_img.name):
                        if not installer.has_image():
                            installer.build_image()
                    installer.install(creator.interpreter.version_info)
                except Exception:  # noqa: BLE001
                    exceptions[name] = sys.exc_info()

            threads = [
                Thread(target=_install, args=(n, w)) for n, w in name_to_whl.items()
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            if exceptions:
                messages = [
                    f"failed to build image {', '.join(exceptions.keys())} because:"
                ]
                for value in exceptions.values():
                    exc_type, exc_value, exc_traceback = value
                    messages.append(
                        "".join(
                            traceback.format_exception(
                                exc_type, exc_value, exc_traceback
                            )
                        )
                    )
                raise RuntimeError("\n".join(messages))

    @contextmanager
    def _get_seed_wheels(self, creator):  # noqa: C901
        name_to_whl, lock, fail = {}, Lock(), {}

        def _get(distribution, version):
            for_py_version = creator.interpreter.version_release_str
            failure, result = None, None
            # fallback to download in case the exact version is not available
            for download in [True] if self.download else [False, True]:
                failure = None
                try:
                    result = get_wheel(
                        distribution=distribution,
                        version=version,
                        for_py_version=for_py_version,
                        search_dirs=self.extra_search_dir,
                        download=download,
                        app_data=self.app_data,
                        do_periodic_update=self.periodic_update,
                        env=self.env,
                    )
                    if result is not None:
                        break
                except Exception as exception:
                    logging.exception("fail")
                    failure = exception
            if failure:
                if isinstance(failure, CalledProcessError):
                    msg = f"failed to download {distribution}"
                    if version is not None:
                        msg += f" version {version}"
                    msg += f", pip download exit code {failure.returncode}"
                    output = failure.output + failure.stderr
                    if output:
                        msg += "\n"
                        msg += output
                else:
                    msg = repr(failure)
                logging.error(msg)
                with lock:
                    fail[distribution] = version
            else:
                with lock:
                    name_to_whl[distribution] = result

        threads = [
            Thread(target=_get, args=(distribution, version))
            for distribution, version in self.distribution_to_versions().items()
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if fail:
            msg = f"seed failed due to failing to download wheels {', '.join(fail.keys())}"
            raise RuntimeError(msg)
        yield name_to_whl

    def installer_class(self, pip_version_tuple):
        if (
            self.symlinks and pip_version_tuple and pip_version_tuple >= (19, 3)
        ):  # symlink support requires pip 19.3+
            return SymlinkPipInstall
        return CopyPipInstall

    def __repr__(self) -> str:
        msg = f", via={'symlink' if self.symlinks else 'copy'}, app_data_dir={self.app_data}"
        base = super().__repr__()
        return f"{base[:-1]}{msg}{base[-1]}"


__all__ = [
    "FromAppData",
]
