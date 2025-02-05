from inspect import signature
from typing import Annotated

from fastapi.dependencies.utils import ParamDetails, analyze_param
from pydantic import Field


def func(user: Annotated[int, Field(strict=True)]): ...


def test_analyze_param():
    result = analyze_param(
        param_name="user",
        annotation=signature(func).parameters["user"].annotation,
        value=object(),
        is_path_param=False,
    )
    assert isinstance(result, ParamDetails)
    assert result.field.field_info.annotation is int
