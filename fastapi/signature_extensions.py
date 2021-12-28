from inspect import Parameter
from typing import Any, Callable, Dict, Iterable, Set

from fastapi.types import DecoratedCallable


def extra_parameters(
    **kwargs: Dict[str, Any]
) -> Callable[[DecoratedCallable], DecoratedCallable]:

    extra_params: Dict[str, Parameter] = dict()
    for name, value in kwargs.items():
        extra_param = Parameter(name, Parameter.KEYWORD_ONLY)
        if isinstance(value, Iterable):
            # consider value to be (annotation, default)
            annotation_default = tuple(value)
            if len(annotation_default) != 2:
                raise ValueError(
                    "Expected an Iterable of length 2: (annotation, default)"
                )
            extra_param = extra_param.replace(
                annotation=annotation_default[0], default=annotation_default[1]
            )
        else:
            # consider value to be annotation
            extra_param = extra_param.replace(annotation=value)
        extra_params[name] = extra_param

    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        extra: Dict[str, Any] = getattr(
            func, "__endpoint_signature_extra_parameters__", dict()
        )
        func.__endpoint_signature_extra_parameters__ = extra
        func.__endpoint_signature_extra_parameters__.update(**extra_params)
        return func

    return decorator


def exclude_parameters(*args: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        exclude: Set[str] = getattr(
            func, "__endpoint_signature_excluded_parameters__", set()
        )
        func.__endpoint_signature_excluded_parameters__ = exclude.union(args)
        return func
    return decorator
