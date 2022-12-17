from typing import Any, Dict, Mapping, Tuple, Type, Union

SingleParameterSpec = Union[
    Mapping[str, Union[Type[Any], Any]],
    Tuple[Type[Any], Any],
    Type[Any],
]
ParameterSpec = Dict[str, SingleParameterSpec]
