from __future__ import annotations

from pathlib import Path


def handle_store_python(meta, interpreter):
    if is_store_python(interpreter):
        meta.symlink_error = (
            "Windows Store Python does not support virtual environments via symlink"
        )
    return meta


def is_store_python(interpreter):
    parts = Path(interpreter.system_executable).parts
    return (
        len(parts) > 4  # noqa: PLR2004
        and parts[-4] == "Microsoft"
        and parts[-3] == "WindowsApps"
        and parts[-2].startswith("PythonSoftwareFoundation.Python.3.")
        and parts[-1].startswith("python")
    )


__all__ = [
    "handle_store_python",
    "is_store_python",
]
