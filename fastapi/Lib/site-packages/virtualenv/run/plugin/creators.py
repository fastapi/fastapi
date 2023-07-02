from __future__ import annotations

from collections import OrderedDict, defaultdict, namedtuple

from virtualenv.create.describe import Describe
from virtualenv.create.via_global_ref.builtin.builtin_way import VirtualenvBuiltin

from .base import ComponentBuilder

CreatorInfo = namedtuple(
    "CreatorInfo", ["key_to_class", "key_to_meta", "describe", "builtin_key"]
)


class CreatorSelector(ComponentBuilder):
    def __init__(self, interpreter, parser) -> None:
        (
            creators,
            self.key_to_meta,
            self.describe,
            self.builtin_key,
        ) = self.for_interpreter(interpreter)
        super().__init__(interpreter, parser, "creator", creators)

    @classmethod
    def for_interpreter(cls, interpreter):
        key_to_class, key_to_meta, builtin_key, describe = OrderedDict(), {}, None, None
        errors = defaultdict(list)
        for key, creator_class in cls.options("virtualenv.create").items():
            if key == "builtin":
                msg = "builtin creator is a reserved name"
                raise RuntimeError(msg)
            meta = creator_class.can_create(interpreter)
            if meta:
                if meta.error:
                    errors[meta.error].append(creator_class)
                else:
                    if "builtin" not in key_to_class and issubclass(
                        creator_class, VirtualenvBuiltin
                    ):
                        builtin_key = key
                        key_to_class["builtin"] = creator_class
                        key_to_meta["builtin"] = meta
                    key_to_class[key] = creator_class
                    key_to_meta[key] = meta
            if (
                describe is None
                and issubclass(creator_class, Describe)
                and creator_class.can_describe(interpreter)
            ):
                describe = creator_class
        if not key_to_meta:
            if errors:
                rows = [
                    f"{k} for creators {', '.join(i.__name__ for i in v)}"
                    for k, v in errors.items()
                ]
                raise RuntimeError("\n".join(rows))
            msg = f"No virtualenv implementation for {interpreter}"
            raise RuntimeError(msg)
        return CreatorInfo(
            key_to_class=key_to_class,
            key_to_meta=key_to_meta,
            describe=describe,
            builtin_key=builtin_key,
        )

    def add_selector_arg_parse(self, name, choices):
        # prefer the built-in venv if present, otherwise fallback to first defined type
        choices = sorted(choices, key=lambda a: 0 if a == "builtin" else 1)
        default_value = self._get_default(choices)
        self.parser.add_argument(
            f"--{name}",
            choices=choices,
            default=default_value,
            required=False,
            help=f"create environment via{'' if self.builtin_key is None else f' (builtin = {self.builtin_key})'}",
        )

    @staticmethod
    def _get_default(choices):
        return next(iter(choices))

    def populate_selected_argparse(self, selected, app_data):
        self.parser.description = f"options for {self.name} {selected}"
        self._impl_class.add_parser_arguments(
            self.parser, self.interpreter, self.key_to_meta[selected], app_data
        )

    def create(self, options):
        options.meta = self.key_to_meta[getattr(options, self.name)]
        if not issubclass(self._impl_class, Describe):
            options.describe = self.describe(options, self.interpreter)
        return super().create(options)


__all__ = [
    "CreatorSelector",
    "CreatorInfo",
]
