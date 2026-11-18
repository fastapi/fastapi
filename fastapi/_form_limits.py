from typing import Annotated

from annotated_doc import Doc
from pydantic import ConfigDict, NonNegativeInt, TypeAdapter, with_config
from typing_extensions import TypedDict


@with_config(ConfigDict(strict=True, extra="forbid"))
class _FormLimits(TypedDict, total=False):
    """Limits for automatic parsing of `Form`, `File`, and `UploadFile` parameters."""

    max_fields: Annotated[
        NonNegativeInt, Doc("Maximum number of non-file form fields.")
    ]
    max_files: Annotated[
        NonNegativeInt, Doc("Maximum number of files in a multipart form.")
    ]
    max_part_size: Annotated[
        NonNegativeInt, Doc("Maximum size of a non-file field in bytes.")
    ]


_form_limits_adapter = TypeAdapter(_FormLimits)


def _validate_form_limits(limits: _FormLimits | None) -> _FormLimits:
    return {} if limits is None else _form_limits_adapter.validate_python(limits)
