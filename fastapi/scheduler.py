import asyncio
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Tuple

from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.background import P


class TaskScheduler:
    def __init__(self) -> None:
        ...

    async def schedule_task(
        self,
        func: Callable[P, Any],
        execute_at: datetime,
        args: Optional[Tuple[Any]],
        kwargs: Optional[Dict[str, Any]],
    ) -> None:
        now = datetime.now()
        if execute_at <= now:
            await self.execute_function(func, args, kwargs)
        else:
            delay = (execute_at - now).total_seconds()
            await asyncio.sleep(delay)
            await self.execute_function(func, args, kwargs)

    async def execute_function(
        self,
        func: Callable[P, Any],
        args: Optional[Tuple[Any]],
        kwargs: Optional[Dict[str, Any]],
    ) -> None:
        is_async = is_async_callable(func)
        if is_async:
            await func(*args, **kwargs)
        else:
            await run_in_threadpool(func, *args, **kwargs)

    def add_task(
        self,
        func: Callable[P, Any],
        execute_at: datetime,
        args: Optional[Tuple[Any]] = (),
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        if kwargs is None:
            kwargs = {}
        asyncio.create_task(self.schedule_task(func, execute_at, args, kwargs))


def get_scheduler() -> TaskScheduler:
    return TaskScheduler()
