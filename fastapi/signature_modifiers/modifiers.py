from typing import Callable

from fastapi.types import DecoratedCallable

from .types import SingleParameterSpec
from .utils import SignatureModifiers, transform_parameters_dict


def extra_parameters(
    **kwargs: SingleParameterSpec,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    extra_params = transform_parameters_dict(kwargs)

    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        sign_modifiers = SignatureModifiers.of(func)
        sign_modifiers.extra_parameters.update(**extra_params)
        return func

    return decorator
