"""Top-level package for sniffio."""

__all__ = [
    "current_async_library",
    "AsyncLibraryNotFoundError",
    "current_async_library_cvar",
]

from ._impl import (
    AsyncLibraryNotFoundError,
    current_async_library,
    current_async_library_cvar,
    thread_local,
)
from ._version import __version__
