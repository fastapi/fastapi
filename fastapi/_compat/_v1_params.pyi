
from typing import Any

class Param:
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...
    in_: Any

class Body(Param):
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...

class Form(Body):
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...

class File(Form):
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...

class Path(Param):
    def __init__(self, annotation: Any = ..., default: Any = ..., alias: str = ..., **kwargs: Any) -> None: ...
    alias: str
    default: Any

class Query(Param):
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...

class Header(Param):
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...

class Cookie(Param):
    def __init__(self, annotation: Any = ..., default: Any = ..., **kwargs: Any) -> None: ...
