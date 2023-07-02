import collections
import contextlib
import os.path
import re
import sys


class ValidationError(ValueError):
    def __init__(self, error_msg, ctx=None):
        super().__init__(error_msg)
        self.error_msg = error_msg
        self.ctx = ctx

    def __str__(self):
        out = "\n"
        err = self
        while err.ctx is not None:
            out += f"==> {err.ctx}\n"
            err = err.error_msg
        out += f"=====> {err.error_msg}"
        return out


MISSING = collections.namedtuple("Missing", ())()
type(MISSING).__repr__ = lambda self: "MISSING"


@contextlib.contextmanager
def validate_context(msg):
    try:
        yield
    except ValidationError as e:
        _, _, tb = sys.exc_info()
        raise ValidationError(e, ctx=msg).with_traceback(tb) from None


@contextlib.contextmanager
def reraise_as(tp):
    try:
        yield
    except ValidationError as e:
        _, _, tb = sys.exc_info()
        raise tp(e).with_traceback(tb) from None


def _dct_noop(self, dct):
    pass


def _check_optional(self, dct):
    if self.key not in dct:
        return
    with validate_context(f"At key: {self.key}"):
        self.check_fn(dct[self.key])


def _apply_default_optional(self, dct):
    dct.setdefault(self.key, self.default)


def _remove_default_optional(self, dct):
    if dct.get(self.key, MISSING) == self.default:
        del dct[self.key]


def _require_key(self, dct):
    if self.key not in dct:
        raise ValidationError(f"Missing required key: {self.key}")


def _check_required(self, dct):
    _require_key(self, dct)
    _check_optional(self, dct)


@property
def _check_fn_recurse(self):
    def check_fn(val):
        validate(val, self.schema)

    return check_fn


def _apply_default_required_recurse(self, dct):
    dct[self.key] = apply_defaults(dct[self.key], self.schema)


def _remove_default_required_recurse(self, dct):
    dct[self.key] = remove_defaults(dct[self.key], self.schema)


def _apply_default_optional_recurse(self, dct):
    if self.key not in dct:
        _apply_default_optional(self, dct)
    _apply_default_required_recurse(self, dct)


def _remove_default_optional_recurse(self, dct):
    if self.key in dct:
        _remove_default_required_recurse(self, dct)
        _remove_default_optional(self, dct)


def _get_check_conditional(inner):
    def _check_conditional(self, dct):
        if dct.get(self.condition_key, MISSING) == self.condition_value:
            inner(self, dct)
        elif self.condition_key in dct and self.ensure_absent and self.key in dct:
            if hasattr(self.condition_value, "describe_opposite"):
                explanation = self.condition_value.describe_opposite()
            else:
                explanation = f"is not {self.condition_value!r}"
            raise ValidationError(
                f"Expected {self.key} to be absent when {self.condition_key} "
                f"{explanation}, found {self.key}: {dct[self.key]!r}",
            )

    return _check_conditional


def _apply_default_conditional_optional(self, dct):
    if dct.get(self.condition_key, MISSING) == self.condition_value:
        _apply_default_optional(self, dct)


def _remove_default_conditional_optional(self, dct):
    if dct.get(self.condition_key, MISSING) == self.condition_value:
        _remove_default_optional(self, dct)


def _apply_default_conditional_recurse(self, dct):
    if dct.get(self.condition_key, MISSING) == self.condition_value:
        _apply_default_required_recurse(self, dct)


def _remove_default_conditional_recurse(self, dct):
    if dct.get(self.condition_key, MISSING) == self.condition_value:
        _remove_default_required_recurse(self, dct)


def _no_additional_keys_check(self, dct):
    extra = sorted(set(dct) - set(self.keys))
    if extra:
        extra_s = ", ".join(str(x) for x in extra)
        keys_s = ", ".join(str(x) for x in self.keys)
        raise ValidationError(
            f"Additional keys found: {extra_s}.  "
            f"Only these keys are allowed: {keys_s}",
        )


def _warn_additional_keys_check(self, dct):
    extra = sorted(set(dct) - set(self.keys))
    if extra:
        self.callback(extra, self.keys, dct)


Required = collections.namedtuple("Required", ("key", "check_fn"))
Required.check = _check_required
Required.apply_default = _dct_noop
Required.remove_default = _dct_noop
RequiredRecurse = collections.namedtuple("RequiredRecurse", ("key", "schema"))
RequiredRecurse.check = _check_required
RequiredRecurse.check_fn = _check_fn_recurse
RequiredRecurse.apply_default = _apply_default_required_recurse
RequiredRecurse.remove_default = _remove_default_required_recurse
Optional = collections.namedtuple("Optional", ("key", "check_fn", "default"))
Optional.check = _check_optional
Optional.apply_default = _apply_default_optional
Optional.remove_default = _remove_default_optional
OptionalRecurse = collections.namedtuple(
    "OptionalRecurse",
    ("key", "schema", "default"),
)
OptionalRecurse.check = _check_optional
OptionalRecurse.check_fn = _check_fn_recurse
OptionalRecurse.apply_default = _apply_default_optional_recurse
OptionalRecurse.remove_default = _remove_default_optional_recurse
OptionalNoDefault = collections.namedtuple(
    "OptionalNoDefault",
    ("key", "check_fn"),
)
OptionalNoDefault.check = _check_optional
OptionalNoDefault.apply_default = _dct_noop
OptionalNoDefault.remove_default = _dct_noop
Conditional = collections.namedtuple(
    "Conditional",
    ("key", "check_fn", "condition_key", "condition_value", "ensure_absent"),
)
Conditional.__new__.__defaults__ = (False,)
Conditional.check = _get_check_conditional(_check_required)
Conditional.apply_default = _dct_noop
Conditional.remove_default = _dct_noop
ConditionalOptional = collections.namedtuple(
    "ConditionalOptional",
    (
        "key",
        "check_fn",
        "default",
        "condition_key",
        "condition_value",
        "ensure_absent",
    ),
)
ConditionalOptional.__new__.__defaults__ = (False,)
ConditionalOptional.check = _get_check_conditional(_check_optional)
ConditionalOptional.apply_default = _apply_default_conditional_optional
ConditionalOptional.remove_default = _remove_default_conditional_optional
ConditionalRecurse = collections.namedtuple(
    "ConditionalRecurse",
    ("key", "schema", "condition_key", "condition_value", "ensure_absent"),
)
ConditionalRecurse.__new__.__defaults__ = (False,)
ConditionalRecurse.check = _get_check_conditional(_check_required)
ConditionalRecurse.check_fn = _check_fn_recurse
ConditionalRecurse.apply_default = _apply_default_conditional_recurse
ConditionalRecurse.remove_default = _remove_default_conditional_recurse
NoAdditionalKeys = collections.namedtuple("NoAdditionalKeys", ("keys",))
NoAdditionalKeys.check = _no_additional_keys_check
NoAdditionalKeys.apply_default = _dct_noop
NoAdditionalKeys.remove_default = _dct_noop
WarnAdditionalKeys = collections.namedtuple(
    "WarnAdditionalKeys",
    ("keys", "callback"),
)
WarnAdditionalKeys.check = _warn_additional_keys_check
WarnAdditionalKeys.apply_default = _dct_noop
WarnAdditionalKeys.remove_default = _dct_noop


class Map(collections.namedtuple("Map", ("object_name", "id_key", "items"))):
    __slots__ = ()

    def __new__(cls, object_name, id_key, *items):
        return super().__new__(cls, object_name, id_key, items)

    def check(self, v):
        if not isinstance(v, dict):
            raise ValidationError(
                f"Expected a {self.object_name} map but got a " f"{type(v).__name__}",
            )
        if self.id_key is None:
            context = f"At {self.object_name}()"
        else:
            key_v_s = v.get(self.id_key, MISSING)
            context = f"At {self.object_name}({self.id_key}={key_v_s!r})"
        with validate_context(context):
            for item in self.items:
                item.check(v)

    def apply_defaults(self, v):
        ret = v.copy()
        for item in self.items:
            item.apply_default(ret)
        return ret

    def remove_defaults(self, v):
        ret = v.copy()
        for item in self.items:
            item.remove_default(ret)
        return ret


class Array(collections.namedtuple("Array", ("of", "allow_empty"))):
    __slots__ = ()

    def __new__(cls, of, allow_empty=True):
        return super().__new__(cls, of=of, allow_empty=allow_empty)

    def check(self, v):
        check_array(check_any)(v)
        if not self.allow_empty and not v:
            raise ValidationError(
                f"Expected at least 1 '{self.of.object_name}'",
            )
        for val in v:
            validate(val, self.of)

    def apply_defaults(self, v):
        return [apply_defaults(val, self.of) for val in v]

    def remove_defaults(self, v):
        return [remove_defaults(val, self.of) for val in v]


class Not(collections.namedtuple("Not", ("val",))):
    __slots__ = ()

    def describe_opposite(self):
        return f"is {self.val!r}"

    def __eq__(self, other):
        return other is not MISSING and other != self.val


class NotIn(collections.namedtuple("NotIn", ("values",))):
    __slots__ = ()

    def __new__(cls, *values):
        return super().__new__(cls, values=values)

    def describe_opposite(self):
        return f"is any of {self.values!r}"

    def __eq__(self, other):
        return other is not MISSING and other not in self.values


class In(collections.namedtuple("In", ("values",))):
    __slots__ = ()

    def __new__(cls, *values):
        return super().__new__(cls, values=values)

    def describe_opposite(self):
        return f"is not any of {self.values!r}"

    def __eq__(self, other):
        return other is not MISSING and other in self.values


def check_any(_):
    pass


def check_type(tp, typename=None):
    def check_type_fn(v):
        if not isinstance(v, tp):
            typename_s = typename or tp.__name__
            raise ValidationError(
                f"Expected {typename_s} got {type(v).__name__}",
            )

    return check_type_fn


check_bool = check_type(bool)
check_bytes = check_type(bytes)
check_int = check_type(int)
check_string = check_type(str, typename="string")
check_text = check_type(str, typename="text")


def check_one_of(possible):
    def check_one_of_fn(v):
        if v not in possible:
            possible_s = ", ".join(str(x) for x in sorted(possible))
            raise ValidationError(
                f"Expected one of {possible_s} but got: {v!r}",
            )

    return check_one_of_fn


def check_regex(v):
    try:
        re.compile(v)
    except re.error:
        raise ValidationError(f"{v!r} is not a valid python regex")


def check_array(inner_check):
    def check_array_fn(v):
        if not isinstance(v, (list, tuple)):
            raise ValidationError(
                f"Expected array but got {type(v).__name__!r}",
            )

        for i, val in enumerate(v):
            with validate_context(f"At index {i}"):
                inner_check(val)

    return check_array_fn


def check_and(*fns):
    def check(v):
        for fn in fns:
            fn(v)

    return check


def validate(v, schema):
    schema.check(v)
    return v


def apply_defaults(v, schema):
    return schema.apply_defaults(v)


def remove_defaults(v, schema):
    return schema.remove_defaults(v)


def load_from_filename(
    filename,
    schema,
    load_strategy,
    exc_tp=ValidationError,
):
    with reraise_as(exc_tp):
        if not os.path.isfile(filename):
            raise ValidationError(f"{filename} is not a file")

        with validate_context(f"File {filename}"):
            try:
                with open(filename, encoding="utf-8") as f:
                    contents = f.read()
            except UnicodeDecodeError as e:
                raise ValidationError(str(e))

            try:
                data = load_strategy(contents)
            except Exception as e:
                raise ValidationError(str(e))

            validate(data, schema)
            return apply_defaults(data, schema)
