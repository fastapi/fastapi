import enum
from typing import Tuple, Callable, Any


DependencyCacheKey = Tuple[Callable[..., Any], Tuple[str]]


class DependencyCacheScope(enum.Enum):
    app = "app"
    request = True  # for backwards compatibility
    nocache = False  # for backwards compatibility
