from types import FrameType
from typing import Any

from _typeshed import StrOrBytesPath

from . import tasks

def _task_repr_info(task: tasks.Task[Any]) -> list[str]: ...  # undocumented
def _task_get_stack(
    task: tasks.Task[Any], limit: int | None
) -> list[FrameType]: ...  # undocumented
def _task_print_stack(
    task: tasks.Task[Any], limit: int | None, file: StrOrBytesPath
) -> None: ...  # undocumented
