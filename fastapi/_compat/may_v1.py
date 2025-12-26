from collections.abc import Sequence
from typing import Any, Union

from pydantic.v1 import BaseModel as BaseModel
from pydantic.v1.fields import ModelField as ModelField


def _regenerate_error_with_loc(
    *, errors: Sequence[Any], loc_prefix: tuple[Union[str, int], ...]
) -> list[dict[str, Any]]:
    updated_loc_errors: list[Any] = [
        {**err, "loc": loc_prefix + err.get("loc", ())} for err in errors
    ]

    return updated_loc_errors
