from typing import Any, Dict, Iterable, Mapping, Type, Union

SingleParameterSpec = Union[Mapping[str, Any], Iterable[Union[str, Any]], Type[Any]]
ParameterSpec = Dict[str, SingleParameterSpec]
