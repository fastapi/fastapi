import ast
import inspect
import re
import warnings
from dataclasses import is_dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    MutableMapping,
    Optional,
    Set,
    Type,
    Union,
    cast,
)
from weakref import WeakKeyDictionary

import fastapi
from fastapi._compat import (
    PYDANTIC_V2,
    BaseConfig,
    ModelField,
    PydanticSchemaGenerationError,
    Undefined,
    UndefinedType,
    Validator,
    annotation_is_pydantic_v1,
    lenient_issubclass,
    may_v1,
)
from fastapi.datastructures import DefaultPlaceholder, DefaultType
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import Literal

if TYPE_CHECKING:  # pragma: nocover
    from .routing import APIRoute

# Cache for `create_cloned_field`
_CLONED_TYPES_CACHE: MutableMapping[Type[BaseModel], Type[BaseModel]] = (
    WeakKeyDictionary()
)


def is_body_allowed_for_status_code(status_code: Union[int, str, None]) -> bool:
    if status_code is None:
        return True
    # Ref: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#patterned-fields-1
    if status_code in {
        "default",
        "1XX",
        "2XX",
        "3XX",
        "4XX",
        "5XX",
    }:
        return True
    current_status_code = int(status_code)
    return not (current_status_code < 200 or current_status_code in {204, 205, 304})


def get_path_param_names(path: str) -> Set[str]:
    return set(re.findall("{(.*?)}", path))


_invalid_args_message = (
    "Invalid args for response field! Hint: "
    "check that {type_} is a valid Pydantic field type. "
    "If you are using a return type annotation that is not a valid Pydantic "
    "field (e.g. Union[Response, dict, None]) you can disable generating the "
    "response model from the type annotation with the path operation decorator "
    "parameter response_model=None. Read more: "
    "https://fastapi.tiangolo.com/tutorial/response-model/"
)


def create_model_field(
    name: str,
    type_: Any,
    class_validators: Optional[Dict[str, Validator]] = None,
    default: Optional[Any] = Undefined,
    required: Union[bool, UndefinedType] = Undefined,
    model_config: Union[Type[BaseConfig], None] = None,
    field_info: Optional[FieldInfo] = None,
    alias: Optional[str] = None,
    mode: Literal["validation", "serialization"] = "validation",
    version: Literal["1", "auto"] = "auto",
) -> ModelField:
    class_validators = class_validators or {}

    v1_model_config = may_v1.BaseConfig
    v1_field_info = field_info or may_v1.FieldInfo()
    v1_kwargs = {
        "name": name,
        "field_info": v1_field_info,
        "type_": type_,
        "class_validators": class_validators,
        "default": default,
        "required": required,
        "model_config": v1_model_config,
        "alias": alias,
    }

    if (
        annotation_is_pydantic_v1(type_)
        or isinstance(field_info, may_v1.FieldInfo)
        or version == "1"
    ):
        from fastapi._compat import v1

        try:
            return v1.ModelField(**v1_kwargs)  # type: ignore[no-any-return]
        except RuntimeError:
            raise fastapi.exceptions.FastAPIError(
                _invalid_args_message.format(type_=type_)
            ) from None
    elif PYDANTIC_V2:
        from ._compat import v2

        field_info = field_info or FieldInfo(
            annotation=type_, default=default, alias=alias
        )
        kwargs = {"mode": mode, "name": name, "field_info": field_info}
        try:
            return v2.ModelField(**kwargs)  # type: ignore[return-value,arg-type]
        except PydanticSchemaGenerationError:
            raise fastapi.exceptions.FastAPIError(
                _invalid_args_message.format(type_=type_)
            ) from None
    # Pydantic v2 is not installed, but it's not a Pydantic v1 ModelField, it could be
    # a Pydantic v1 type, like a constrained int
    from fastapi._compat import v1

    try:
        return v1.ModelField(**v1_kwargs)  # type: ignore[no-any-return]
    except RuntimeError:
        raise fastapi.exceptions.FastAPIError(
            _invalid_args_message.format(type_=type_)
        ) from None


def create_cloned_field(
    field: ModelField,
    *,
    cloned_types: Optional[MutableMapping[Type[BaseModel], Type[BaseModel]]] = None,
) -> ModelField:
    if PYDANTIC_V2:
        from ._compat import v2

        if isinstance(field, v2.ModelField):
            return field

    from fastapi._compat import v1

    # cloned_types caches already cloned types to support recursive models and improve
    # performance by avoiding unnecessary cloning
    if cloned_types is None:
        cloned_types = _CLONED_TYPES_CACHE

    original_type = field.type_
    if is_dataclass(original_type) and hasattr(original_type, "__pydantic_model__"):
        original_type = original_type.__pydantic_model__
    use_type = original_type
    if lenient_issubclass(original_type, v1.BaseModel):
        original_type = cast(Type[v1.BaseModel], original_type)
        use_type = cloned_types.get(original_type)
        if use_type is None:
            use_type = v1.create_model(original_type.__name__, __base__=original_type)
            cloned_types[original_type] = use_type
            for f in original_type.__fields__.values():
                use_type.__fields__[f.name] = create_cloned_field(
                    f,
                    cloned_types=cloned_types,
                )
    new_field = create_model_field(name=field.name, type_=use_type, version="1")
    new_field.has_alias = field.has_alias  # type: ignore[attr-defined]
    new_field.alias = field.alias  # type: ignore[misc]
    new_field.class_validators = field.class_validators  # type: ignore[attr-defined]
    new_field.default = field.default  # type: ignore[misc]
    new_field.default_factory = field.default_factory  # type: ignore[attr-defined]
    new_field.required = field.required  # type: ignore[misc]
    new_field.model_config = field.model_config  # type: ignore[attr-defined]
    new_field.field_info = field.field_info
    new_field.allow_none = field.allow_none  # type: ignore[attr-defined]
    new_field.validate_always = field.validate_always  # type: ignore[attr-defined]
    if field.sub_fields:  # type: ignore[attr-defined]
        new_field.sub_fields = [  # type: ignore[attr-defined]
            create_cloned_field(sub_field, cloned_types=cloned_types)
            for sub_field in field.sub_fields  # type: ignore[attr-defined]
        ]
    if field.key_field:  # type: ignore[attr-defined]
        new_field.key_field = create_cloned_field(  # type: ignore[attr-defined]
            field.key_field,  # type: ignore[attr-defined]
            cloned_types=cloned_types,
        )
    new_field.validators = field.validators  # type: ignore[attr-defined]
    new_field.pre_validators = field.pre_validators  # type: ignore[attr-defined]
    new_field.post_validators = field.post_validators  # type: ignore[attr-defined]
    new_field.parse_json = field.parse_json  # type: ignore[attr-defined]
    new_field.shape = field.shape  # type: ignore[attr-defined]
    new_field.populate_validators()  # type: ignore[attr-defined]
    return new_field


def generate_operation_id_for_path(
    *, name: str, path: str, method: str
) -> str:  # pragma: nocover
    warnings.warn(
        "fastapi.utils.generate_operation_id_for_path() was deprecated, "
        "it is not used internally, and will be removed soon",
        DeprecationWarning,
        stacklevel=2,
    )
    operation_id = f"{name}{path}"
    operation_id = re.sub(r"\W", "_", operation_id)
    operation_id = f"{operation_id}_{method.lower()}"
    return operation_id


def generate_unique_id(route: "APIRoute") -> str:
    operation_id = f"{route.name}{route.path_format}"
    operation_id = re.sub(r"\W", "_", operation_id)
    assert route.methods
    operation_id = f"{operation_id}_{list(route.methods)[0].lower()}"
    return operation_id


def deep_dict_update(main_dict: Dict[Any, Any], update_dict: Dict[Any, Any]) -> None:
    for key, value in update_dict.items():
        if (
            key in main_dict
            and isinstance(main_dict[key], dict)
            and isinstance(value, dict)
        ):
            deep_dict_update(main_dict[key], value)
        elif (
            key in main_dict
            and isinstance(main_dict[key], list)
            and isinstance(update_dict[key], list)
        ):
            main_dict[key] = main_dict[key] + update_dict[key]
        else:
            main_dict[key] = value


def get_value_or_default(
    first_item: Union[DefaultPlaceholder, DefaultType],
    *extra_items: Union[DefaultPlaceholder, DefaultType],
) -> Union[DefaultPlaceholder, DefaultType]:
    """
    Pass items or `DefaultPlaceholder`s by descending priority.

    The first one to _not_ be a `DefaultPlaceholder` will be returned.

    Otherwise, the first item (a `DefaultPlaceholder`) will be returned.
    """
    items = (first_item,) + extra_items
    for item in items:
        if not isinstance(item, DefaultPlaceholder):
            return item
    return first_item


def _infer_type_from_ast(
    node: ast.AST,
    func_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    context_name: str,
) -> Any:
    if isinstance(node, ast.Constant):
        return type(node.value)

    if isinstance(node, ast.List):
        if not node.elts:
            return List[Any]

        first_type = _infer_type_from_ast(node.elts[0], func_def, context_name + "Item")

        for elt in node.elts[1:]:
            current_type = _infer_type_from_ast(elt, func_def, context_name + "Item")
            if current_type != first_type:
                return List[Any]

        if first_type is not Any:
            return List[first_type]  # type: ignore
        return List[Any]

    if isinstance(node, ast.BinOp):
        left_type = _infer_type_from_ast(node.left, func_def, context_name)
        right_type = _infer_type_from_ast(node.right, func_def, context_name)
        if left_type == right_type and left_type in (int, float, str):
            return left_type
        if {left_type, right_type} == {int, float}:
            return float

    if isinstance(node, ast.Compare):
        return bool

    if isinstance(node, ast.Dict):
        fields = {}
        for key, value in zip(node.keys, node.values):
            if not isinstance(key, ast.Constant):
                continue
            field_name = key.value
            field_type = _infer_type_from_ast(
                value, func_def, context_name + "_" + str(field_name)
            )
            fields[field_name] = (field_type, ...)

        if not fields:
            return Dict[str, Any]

        if PYDANTIC_V2:
            from pydantic import create_model
        else:
            from fastapi._compat.v1 import create_model

        return create_model(f"Model_{context_name}", **fields)  # type: ignore[call-overload]

    if isinstance(node, ast.Name):
        arg_name = node.id
        for arg in func_def.args.args:
            if arg.arg != arg_name:
                continue

            if not arg.annotation:
                continue

            if not isinstance(arg.annotation, ast.Name):
                continue

            annotation_id = arg.annotation.id
            if annotation_id == "int":
                return int
            if annotation_id == "str":
                return str
            if annotation_id == "bool":
                return bool
            if annotation_id == "float":
                return float
            if annotation_id == "list":
                return List[Any]
            if annotation_id == "dict":
                return Dict[str, Any]

    return Any


def infer_response_model_from_ast(
    endpoint_function: Any,
) -> Optional[Type[BaseModel]]:
    """
    Analyze the endpoint function's source code to infer a Pydantic model
    from a returned dictionary literal or variable assignment.
    """
    import textwrap

    try:
        source = inspect.getsource(endpoint_function)
    except (OSError, TypeError):
        return None

    source = textwrap.dedent(source)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    if not tree.body:
        return None

    func_def = tree.body[0]
    if not isinstance(func_def, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return None

    return_stmt = None

    nodes_to_visit: List[ast.AST] = list(func_def.body)
    while nodes_to_visit:
        node = nodes_to_visit.pop(0)

        if isinstance(node, ast.Return):
            return_stmt = node
            break

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue

        for child in ast.iter_child_nodes(node):
            nodes_to_visit.append(child)

    if not return_stmt:
        return None

    returned_value = return_stmt.value
    dict_node = None

    if isinstance(returned_value, ast.Dict):
        dict_node = returned_value
    elif isinstance(returned_value, ast.Name):
        variable_name = returned_value.id
        # Find assignment
        for node in func_def.body:
            if (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == variable_name
            ):
                if isinstance(node.value, ast.Dict):
                    dict_node = node.value
                    break
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == variable_name:
                        if isinstance(node.value, ast.Dict):
                            dict_node = node.value
                            break

    if not dict_node:
        return None

    fields = {}
    for key, value in zip(dict_node.keys, dict_node.values):
        if not isinstance(key, ast.Constant):
            continue

        if not isinstance(key.value, str):
            return None

        field_name = key.value

        field_type = _infer_type_from_ast(
            value, func_def, f"{endpoint_function.__name__}_{field_name}"
        )

        fields[field_name] = (field_type, ...)

    if not fields:
        return None

    # Don't create a model if all fields are Any - this provides no additional
    # type information compared to Dict[str, Any] and would override explicit
    # type annotations unnecessarily
    if all(field_type is Any for field_type, _ in fields.values()):
        return None

    if PYDANTIC_V2:
        from pydantic import create_model
    else:
        from fastapi._compat.v1 import create_model

    model_name = f"ResponseModel_{endpoint_function.__name__}"
    try:
        return create_model(model_name, **fields)  # type: ignore[call-overload,no-any-return]
    except Exception:
        return None
