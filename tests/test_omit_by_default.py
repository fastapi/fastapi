import sys
from typing import Dict, List, Optional, Union

import pytest
from pydantic import OnErrorOmit
from typing_extensions import Annotated


def omit_by_default(annotation):
    """A simplified version of the omit_by_default function for testing purposes."""
    origin = getattr(annotation, "__origin__", None)
    args = getattr(annotation, "__args__", ())

    if origin is Annotated:
        new_args = (omit_by_default(args[0]),) + args[1:]
        return Annotated[new_args[0], *new_args[1:]]
    elif origin is Union:
        new_args = tuple(omit_by_default(arg) for arg in args)
        return Union[new_args]
    elif origin in (list, List):
        return List[omit_by_default(args[0])]
    elif origin in (dict, Dict):
        return Dict[args[0], omit_by_default(args[1])]
    else:
        return OnErrorOmit[annotation]


def test_omit_by_default_simple_type():
    result = omit_by_default(int)
    assert result == OnErrorOmit[int]


def test_omit_by_default_union():
    result = omit_by_default(Union[int, str])
    assert result == Union[OnErrorOmit[int], OnErrorOmit[str]]


def test_omit_by_default_optional():
    result = omit_by_default(Optional[int])
    assert result == Union[OnErrorOmit[int], OnErrorOmit[type(None)]]


def test_omit_by_default_annotated():
    result = omit_by_default(Annotated[int, "metadata"])
    origin = result.__origin__ if hasattr(result, "__origin__") else None
    assert origin is Annotated
    args = result.__args__ if hasattr(result, "__args__") else ()
    assert len(args) == 2
    assert args[0] == OnErrorOmit[int]
    assert args[1] == "metadata"


def test_omit_by_default_annotated_union():
    result = omit_by_default(Annotated[Union[int, str], "metadata"])
    origin = result.__origin__ if hasattr(result, "__origin__") else None
    assert origin is Annotated
    args = result.__args__ if hasattr(result, "__args__") else ()
    assert len(args) == 2
    assert args[0] == Union[OnErrorOmit[int], OnErrorOmit[str]]
    assert args[1] == "metadata"


def test_omit_by_default_list():
    result = omit_by_default(List[int])
    assert result == List[OnErrorOmit[int]]


def test_omit_by_default_dict():
    result = omit_by_default(Dict[str, int])
    assert result == Dict[str, OnErrorOmit[int]]


def test_omit_by_default_nested_union():
    result = omit_by_default(Union[int, Union[str, float]])
    assert result == Union[OnErrorOmit[int], OnErrorOmit[Union[str, float]]]


def test_omit_by_default_annotated_with_multiple_metadata():
    result = omit_by_default(Annotated[str, "meta1", "meta2"])
    origin = result.__origin__ if hasattr(result, "__origin__") else None
    assert origin is Annotated
    args = result.__args__ if hasattr(result, "__args__") else ()
    assert len(args) == 3
    assert args[0] == OnErrorOmit[str]
    assert args[1] == "meta1"
    assert args[2] == "meta2"


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason="Union type syntax requires Python 3.10+"
)
def test_omit_by_default_pipe_union():
    annotation = eval("int | str")
    result = omit_by_default(annotation)
    assert result == Union[OnErrorOmit[int], OnErrorOmit[str]]


def test_omit_by_default_complex_nested():
    result = omit_by_default(Annotated[Union[int, Optional[str]], "metadata"])
    origin = result.__origin__ if hasattr(result, "__origin__") else None
    assert origin is Annotated
    args = result.__args__ if hasattr(result, "__args__") else ()
    assert len(args) == 2
    expected_union = Union[OnErrorOmit[int], OnErrorOmit[Union[str, type(None)]]]
    assert args[0] == expected_union
    assert args[1] == "metadata"


def test_omit_by_default_dict_with_union_value():
    result = omit_by_default(Dict[str, Union[int, str]])
    assert result == Dict[str, Union[OnErrorOmit[int], OnErrorOmit[str]]]
