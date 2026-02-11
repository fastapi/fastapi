import types
import typing
import warnings
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import is_dataclass
from typing import (
    Annotated,
    Any,
    TypeGuard,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from fastapi.types import UnionType
from pydantic import BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION
from starlette.datastructures import UploadFile

_T = TypeVar("_T")

# Copy from Pydantic: pydantic/_internal/_typing_extra.py
WithArgsTypes: tuple[Any, ...] = (
    typing._GenericAlias,  # type: ignore[attr-defined]
    types.GenericAlias,
    types.UnionType,
)  # pyright: ignore[reportAttributeAccessIssue]

PYDANTIC_VERSION_MINOR_TUPLE = tuple(int(x) for x in PYDANTIC_VERSION.split(".")[:2])


sequence_annotation_to_type = {
    Sequence: list,
    list: list,
    tuple: tuple,
    set: set,
    frozenset: frozenset,
    deque: deque,
}

sequence_types: tuple[type[Any], ...] = tuple(sequence_annotation_to_type.keys())


# Copy of Pydantic: pydantic/_internal/_utils.py with added TypeGuard
def lenient_issubclass(
    cls: Any, class_or_tuple: type[_T] | tuple[type[_T], ...] | None
) -> TypeGuard[type[_T]]:
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)  # type: ignore[arg-type]
    except TypeError:  # pragma: no cover
        if isinstance(cls, WithArgsTypes):
            return False
        raise  # pragma: no cover


def _annotation_is_sequence(annotation: type[Any] | None) -> bool:
    if lenient_issubclass(annotation, (str, bytes)):
        return False
    return lenient_issubclass(annotation, sequence_types)


def field_annotation_is_sequence(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if field_annotation_is_sequence(arg):
                return True
        return False
    return _annotation_is_sequence(annotation) or _annotation_is_sequence(
        get_origin(annotation)
    )


def value_is_sequence(value: Any) -> bool:
    return isinstance(value, sequence_types) and not isinstance(value, (str, bytes))


def _annotation_is_complex(annotation: type[Any] | None) -> bool:
    return (
        lenient_issubclass(annotation, (BaseModel, Mapping, UploadFile))
        or _annotation_is_sequence(annotation)
        or is_dataclass(annotation)
    )


def field_annotation_is_complex(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        return any(field_annotation_is_complex(arg) for arg in get_args(annotation))

    if origin is Annotated:
        return field_annotation_is_complex(get_args(annotation)[0])

    return (
        _annotation_is_complex(annotation)
        or _annotation_is_complex(origin)
        or hasattr(origin, "__pydantic_core_schema__")
        or hasattr(origin, "__get_pydantic_core_schema__")
    )


def field_annotation_is_scalar(annotation: Any) -> bool:
    # handle Ellipsis here to make tuple[int, ...] work nicely
    return annotation is Ellipsis or not field_annotation_is_complex(annotation)


def field_annotation_is_scalar_sequence(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one_scalar_sequence = False
        for arg in get_args(annotation):
            if field_annotation_is_scalar_sequence(arg):
                at_least_one_scalar_sequence = True
                continue
            elif not field_annotation_is_scalar(arg):
                return False
        return at_least_one_scalar_sequence
    return field_annotation_is_sequence(annotation) and all(
        field_annotation_is_scalar(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def is_bytes_or_nonable_bytes_annotation(annotation: Any) -> bool:
    if lenient_issubclass(annotation, bytes):
        return True
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if lenient_issubclass(arg, bytes):
                return True
    return False


def is_uploadfile_or_nonable_uploadfile_annotation(annotation: Any) -> bool:
    if lenient_issubclass(annotation, UploadFile):
        return True
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if lenient_issubclass(arg, UploadFile):
                return True
    return False


def is_bytes_sequence_annotation(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one = False
        for arg in get_args(annotation):
            if is_bytes_sequence_annotation(arg):
                at_least_one = True
                continue
        return at_least_one
    return field_annotation_is_sequence(annotation) and all(
        is_bytes_or_nonable_bytes_annotation(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def is_uploadfile_sequence_annotation(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one = False
        for arg in get_args(annotation):
            if is_uploadfile_sequence_annotation(arg):
                at_least_one = True
                continue
        return at_least_one
    return field_annotation_is_sequence(annotation) and all(
        is_uploadfile_or_nonable_uploadfile_annotation(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def is_pydantic_v1_model_instance(obj: Any) -> bool:
    # TODO: remove this function once the required version of Pydantic fully
    # removes pydantic.v1
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            from pydantic import v1
    except ImportError:  # pragma: no cover
        return False
    return isinstance(obj, v1.BaseModel)


def is_pydantic_v1_model_class(cls: Any) -> bool:
    # TODO: remove this function once the required version of Pydantic fully
    # removes pydantic.v1
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            from pydantic import v1
    except ImportError:  # pragma: no cover
        return False
    return lenient_issubclass(cls, v1.BaseModel)


def annotation_is_pydantic_v1(annotation: Any) -> bool:
    if is_pydantic_v1_model_class(annotation):
        return True
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if is_pydantic_v1_model_class(arg):
                return True
    if field_annotation_is_sequence(annotation):
        for sub_annotation in get_args(annotation):
            if annotation_is_pydantic_v1(sub_annotation):
                return True
    return False
