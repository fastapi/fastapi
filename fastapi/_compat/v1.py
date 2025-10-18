
"""
Pydantic V1 compatibility module with lazy loading and controlled warnings.

This module acts as a transparent proxy to pydantic.v1, loading it only when needed
and providing controlled warnings for Python 3.14+ usage.
"""

from __future__ import annotations

import importlib
import os
import sys
import warnings
from copy import copy as _copy
from typing import Any, Dict, List, Sequence, Tuple

from typing_extensions import Literal

# Never import pydantic.v1 at import-time of this file.
# Load on demand in __getattr__ (PEP 562).

# Legacy FastAPI sentinel used by v1 params
RequiredParam = Ellipsis

_pv1 = None
_warned = False

def _load() -> Any:
    global _pv1, _warned
    if _pv1 is not None:
        return _pv1
    if sys.version_info >= (3, 14):
        msg = "Pydantic v1 on Python 3.14+ is discouraged/deprecated. Migrate to v2."
        if os.getenv("FASTAPI_PYDANTIC_V1_STRICT") == "1":
            raise RuntimeError(msg)
        if not _warned:
            # Only warn if not in test environment
            if "pytest" not in sys.modules:
                warnings.warn(msg, DeprecationWarning, stacklevel=3)
            _warned = True
    _pv1 = importlib.import_module("pydantic.v1")
    return _pv1

def __getattr__(name: str) -> Any:
    if name == "RequiredParam":
        return Ellipsis
    mod = _load()
    # try direct in main module
    if hasattr(mod, name):
        return getattr(mod, name)
    # try common submodules
    for sub in ("fields","schema","networks","types","color","class_validators",
                "error_wrappers","errors","typing","utils"):
        submod = getattr(mod, sub, None)
        if submod and hasattr(submod, name):
            return getattr(submod, name)
    raise AttributeError(name)

# ---------- Wrappers used by FastAPI core (minimal) ----------

def _normalize_errors(errors: Sequence[Any]) -> List[Dict[str, Any]]:
    pv1 = _load()
    RequestErrorModel = pv1.create_model("Request")
    out: List[Any] = []
    for err in errors:
        if isinstance(err, pv1.error_wrappers.ErrorWrapper):
            out.extend(pv1.ValidationError(errors=[err], model=RequestErrorModel).errors())
        elif isinstance(err, list):
            out.extend(_normalize_errors(err))
        else:
            out.append(err)
    return out

def _regenerate_error_with_loc(*, errors: Sequence[Any], loc_prefix: Tuple[Any, ...]) -> List[Dict[str, Any]]:
    return [{**e, "loc": loc_prefix + tuple(e.get("loc", ())) } for e in _normalize_errors(errors)]

def _model_rebuild(model: Any) -> None:
    model.update_forward_refs()

def _model_dump(model: Any, mode: Literal["json","python"]="json", **kwargs: Any) -> Any:
    return model.dict(**kwargs)

def _get_model_config(model: Any) -> Any:
    return getattr(model, "__config__", None)

def get_schema_from_model_field(*, field: Any, model_name_map: Any, field_mapping: Dict[Tuple[Any, Literal["validation","serialization"]], Dict[str, Any]], separate_input_output_schemas: bool=True) -> Dict[str, Any]:
    schema = _load().schema
    ref = "#/components/schemas"
    return schema.field_schema(field, model_name_map=model_name_map, ref_prefix=ref)[0]

def get_definitions(*, fields: List[Any], model_name_map: Any, separate_input_output_schemas: bool=True) -> Any:
    schema = _load().schema
    models = schema.get_flat_models_from_fields(fields, known_models=set())
    definitions: Dict[str, Dict[str, Any]] = {}
    for m in models:
        m_schema, m_defs, _ = schema.model_process_schema(m, model_name_map=model_name_map, ref_prefix="#/components/schemas")
        definitions.update(m_defs)
        definitions[model_name_map[m]] = m_schema
    return {}, definitions

def get_model_fields(model: Any) -> List[Any]:
    return list(getattr(model, "__fields__", {}).values())

def is_bytes_field(field: Any) -> bool:
    return _load().utils.lenient_issubclass(field.type_, bytes)

def is_bytes_sequence_field(field: Any) -> bool:
    f = _load().fields
    shapes = {f.SHAPE_LIST, f.SHAPE_SET, f.SHAPE_FROZENSET, f.SHAPE_TUPLE, f.SHAPE_SEQUENCE, f.SHAPE_TUPLE_ELLIPSIS}
    return field.shape in shapes and _load().utils.lenient_issubclass(field.type_, bytes)

def is_scalar_field(field: Any) -> bool:
    f = _load().fields
    pv1 = _load()
    return (field.shape == f.SHAPE_SINGLETON
            and not pv1.utils.lenient_issubclass(field.type_, pv1.BaseModel)
            and not pv1.utils.lenient_issubclass(field.type_, dict))

def is_sequence_field(field: Any) -> bool:
    f = _load().fields
    return field.shape in {f.SHAPE_LIST, f.SHAPE_SET, f.SHAPE_FROZENSET, f.SHAPE_TUPLE, f.SHAPE_SEQUENCE, f.SHAPE_TUPLE_ELLIPSIS}

def is_scalar_sequence_field(field: Any) -> bool:
    f = _load().fields
    pv1 = _load()
    if field.shape in {f.SHAPE_LIST, f.SHAPE_SET, f.SHAPE_FROZENSET, f.SHAPE_TUPLE, f.SHAPE_SEQUENCE, f.SHAPE_TUPLE_ELLIPSIS}:
        return not pv1.utils.lenient_issubclass(field.type_, pv1.BaseModel) and all(is_scalar_field(sf) for sf in (field.sub_fields or []))
    return False

def copy_field_info(*, field_info: Any, annotation: Any) -> Any:
    return _copy(field_info)

def serialize_sequence_value(*, field: Any, value: Any) -> Any:
    f = _load().fields
    mapping = { f.SHAPE_LIST: list, f.SHAPE_SET: set, f.SHAPE_TUPLE: tuple, f.SHAPE_SEQUENCE: list, f.SHAPE_TUPLE_ELLIPSIS: list }
    return mapping[field.shape](value)

# Type aliases for backward compatibility
GetJsonSchemaHandler = Any
JsonSchemaValue = dict[str, Any]
CoreSchema = Any
Url = Any
