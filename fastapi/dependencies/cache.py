import enum
from typing import Any, Callable, Optional, Tuple

DependencyCacheKey = Tuple[Optional[Callable[..., Any]], Tuple[str]]


class DependencyCacheScope(enum.Enum):
    app = "app"
    request = True  # for backwards compatibility
    nocache = False  # for backwards compatibility
