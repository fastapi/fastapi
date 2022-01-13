from inspect import Parameter, Signature
from typing import Any, Callable, Dict, Iterable, Mapping, Optional

from .types import ParameterSpec

ALLOWED_PARAMETER_REPLACE_KWARGS = {"annotation", "default"}


def transform_parameters_dict(parameters: ParameterSpec) -> Dict[str, Parameter]:
    extra_params: Dict[str, Parameter] = {}
    for name, value in parameters.items():
        extra_param = Parameter(name, Parameter.KEYWORD_ONLY)
        if isinstance(value, Mapping):
            diff = set(value) - ALLOWED_PARAMETER_REPLACE_KWARGS
            if diff:
                raise ValueError(f"Arguments {diff} are not allowed.")
            extra_param = extra_param.replace(**value)
        elif isinstance(value, Iterable):
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
    return extra_params


class SignatureModifiers:
    _modifiers: Dict[Callable[..., Any], "SignatureModifiers"] = {}

    @classmethod
    def of(cls, call: Callable[..., Any]) -> "SignatureModifiers":
        modifier = cls._modifiers.get(call)
        if modifier is None:
            modifier = SignatureModifiers()
            cls._modifiers[call] = modifier
        return modifier

    def __init__(self) -> None:
        self.extra_parameters: Dict[str, Parameter] = {}
        self.override: Optional[Signature] = None
