from typing import Any, Tuple


class GenericTypeStub:
    class OriginTypeStub:
        __parameters__: Tuple[Any]

    __origin__: OriginTypeStub
    __args__: Tuple[Any]
