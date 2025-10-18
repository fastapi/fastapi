# mypy: disable-error-code=attr-defined
# path: fastapi/_compat/__init__.py

"""
FastAPI Pydantic compatibility layer.

This module provides a v2-first compatibility layer that automatically
detects the Pydantic version and provides the appropriate symbols.
"""

from __future__ import annotations

from typing import Any, Dict

# Import the v1 proxy module - this provides lazy loading and controlled warnings
# Don't import at module level to avoid warnings
# Import legacy compatibility symbols for backward compatibility
# These are now imported dynamically from the appropriate v1/v2 modules
from .shared import PYDANTIC_V2

if PYDANTIC_V2:
    from .v2 import BaseConfig as BaseConfig
    from .v2 import PydanticSchemaGenerationError as PydanticSchemaGenerationError
    from .v2 import RequiredParam as RequiredParam
    from .v2 import Undefined as Undefined
    from .v2 import UndefinedType as UndefinedType
    from .v2 import Url as Url
    from .v2 import Validator as Validator
    from .v2 import _get_model_config as _get_model_config
    from .v2 import _model_dump as _model_dump
    from .v2 import _model_rebuild as _model_rebuild
    from .v2 import copy_field_info as copy_field_info
    from .v2 import create_body_model as create_body_model
    from .v2 import evaluate_forwardref as evaluate_forwardref
    from .v2 import get_annotation_from_field_info as get_annotation_from_field_info
    from .v2 import get_definitions as get_definitions
    from .v2 import get_missing_field_error as get_missing_field_error
    from .v2 import get_schema_from_model_field as get_schema_from_model_field
    from .v2 import is_bytes_field as is_bytes_field
    from .v2 import is_bytes_sequence_field as is_bytes_sequence_field
    from .v2 import is_scalar_field as is_scalar_field
    from .v2 import is_scalar_sequence_field as is_scalar_sequence_field
    from .v2 import is_sequence_field as is_sequence_field
    from .v2 import serialize_sequence_value as serialize_sequence_value
    from .v2 import (
        with_info_plain_validator_function as with_info_plain_validator_function,
    )
else:
    from .v1 import BaseConfig as BaseConfig  # type: ignore[assignment]
    from .v1 import PydanticSchemaGenerationError as PydanticSchemaGenerationError  # type: ignore[assignment]  # noqa: I001
    from .v1 import RequiredParam as RequiredParam  # type: ignore[assignment]
    from .v1 import Undefined as Undefined  # type: ignore[assignment]
    from .v1 import UndefinedType as UndefinedType  # type: ignore[assignment]
    from .v1 import Url as Url  # type: ignore[assignment]
    from .v1 import Validator as Validator  # type: ignore[assignment]
    from .v1 import _get_model_config as _get_model_config
    from .v1 import _model_dump as _model_dump
    from .v1 import _model_rebuild as _model_rebuild
    from .v1 import copy_field_info as copy_field_info
    from .v1 import create_body_model as create_body_model
    from .v1 import evaluate_forwardref as evaluate_forwardref
    from .v1 import get_annotation_from_field_info as get_annotation_from_field_info
    from .v1 import get_definitions as get_definitions
    from .v1 import get_missing_field_error as get_missing_field_error
    from .v1 import get_schema_from_model_field as get_schema_from_model_field
    from .v1 import is_bytes_field as is_bytes_field
    from .v1 import is_bytes_sequence_field as is_bytes_sequence_field
    from .v1 import is_scalar_field as is_scalar_field
    from .v1 import is_scalar_sequence_field as is_scalar_sequence_field
    from .v1 import is_sequence_field as is_sequence_field
    from .v1 import serialize_sequence_value as serialize_sequence_value
    from .v1 import (
        with_info_plain_validator_function as with_info_plain_validator_function,
    )

# Import functions that exist in main.py
from .main import _is_error_wrapper as _is_error_wrapper
from .main import _is_model_class as _is_model_class
from .main import _is_model_field as _is_model_field
from .main import _is_undefined as _is_undefined
from .main import get_cached_model_fields as get_cached_model_fields
from .main import get_compat_model_name_map as get_compat_model_name_map
from .model_field import ModelField as ModelField
from .shared import PYDANTIC_V2 as PYDANTIC_V2
from .shared import PYDANTIC_VERSION_MINOR_TUPLE as PYDANTIC_VERSION_MINOR_TUPLE
from .shared import annotation_is_pydantic_v1 as annotation_is_pydantic_v1
from .shared import field_annotation_is_scalar as field_annotation_is_scalar
from .shared import (
    is_uploadfile_or_nonable_uploadfile_annotation as is_uploadfile_or_nonable_uploadfile_annotation,
)
from .shared import (
    is_uploadfile_sequence_annotation as is_uploadfile_sequence_annotation,
)
from .shared import lenient_issubclass as lenient_issubclass
from .shared import sequence_types as sequence_types
from .shared import value_is_sequence as value_is_sequence

# V1 symbols are available via the v1 proxy module
# Access them directly: from fastapi._compat import v1; v1.CoreSchema
# This avoids import-time access and warnings

# Export V1 symbols as Any to avoid import-time access
CoreSchema = Any
GetJsonSchemaHandler = Any
JsonSchemaValue = Dict[str, Any]


def _normalize_errors(errors: Any) -> Any:
    from importlib import import_module

    v1 = import_module("fastapi._compat.v1")  # proxy lazy
    return v1._normalize_errors(errors)


# Make v1 available as an attribute
def __getattr__(name: str) -> Any:
    if name == "v1":
        # Import directly to avoid recursion
        import importlib

        return importlib.import_module("fastapi._compat.v1")
    raise AttributeError(f"module 'fastapi._compat' has no attribute '{name}'")


# Explicitly export all compatibility symbols
__all__ = [
    "PYDANTIC_V2",
    "BaseConfig",
    "PydanticSchemaGenerationError",
    "RequiredParam",
    "Undefined",
    "UndefinedType",
    "Url",
    "Validator",
    "_get_model_config",
    "_model_dump",
    "_model_rebuild",
    "copy_field_info",
    "create_body_model",
    "evaluate_forwardref",
    "get_annotation_from_field_info",
    "get_definitions",
    "get_missing_field_error",
    "get_schema_from_model_field",
    "is_bytes_field",
    "is_bytes_sequence_field",
    "is_scalar_field",
    "is_scalar_sequence_field",
    "is_sequence_field",
    "serialize_sequence_value",
    "with_info_plain_validator_function",
    "_is_error_wrapper",
    "_is_model_class",
    "_is_model_field",
    "_is_undefined",
    "get_cached_model_fields",
    "get_compat_model_name_map",
    "ModelField",
    "PYDANTIC_VERSION_MINOR_TUPLE",
    "annotation_is_pydantic_v1",
    "field_annotation_is_scalar",
    "is_uploadfile_or_nonable_uploadfile_annotation",
    "is_uploadfile_sequence_annotation",
    "lenient_issubclass",
    "sequence_types",
    "value_is_sequence",
    "CoreSchema",
    "GetJsonSchemaHandler",
    "JsonSchemaValue",
    "_normalize_errors",
    "v1",
]
