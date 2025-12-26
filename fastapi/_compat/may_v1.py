from collections.abc import Sequence
from typing import Any, Union


def _regenerate_error_with_loc(
    *, errors: Sequence[Any], loc_prefix: tuple[Union[str, int], ...]
) -> list[dict[str, Any]]:
    updated_loc_errors: list[Any] = [
        {**err, "loc": loc_prefix + err.get("loc", ())} for err in errors
    ]

    return updated_loc_errors
