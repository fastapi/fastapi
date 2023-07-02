from collections.abc import Awaitable, Callable, Iterable
from typing import Any

from . import events

__all__ = ("staggered_race",)

async def staggered_race(
    coro_fns: Iterable[Callable[[], Awaitable[Any]]],
    delay: float | None,
    *,
    loop: events.AbstractEventLoop | None = None,
) -> tuple[Any, int | None, list[Exception | None]]: ...
