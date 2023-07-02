import inspect
from typing import Any, Callable, Dict, get_type_hints

from .models import ParamMeta


def get_params_from_function(func: Callable[..., Any]) -> Dict[str, ParamMeta]:
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation = param.annotation
        if param.name in type_hints:
            annotation = type_hints[param.name]
        params[param.name] = ParamMeta(
            name=param.name, default=param.default, annotation=annotation
        )
    return params
