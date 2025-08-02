from typing import Any, Tuple

from typing_extensions import Protocol


class GenericTypeProtocol(Protocol):
    class OriginTypeProtocol(Protocol):
        __parameters__: Tuple[Any]

    __origin__: OriginTypeProtocol
    __args__: Tuple[Any]
