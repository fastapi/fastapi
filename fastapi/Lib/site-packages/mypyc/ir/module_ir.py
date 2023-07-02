"""Intermediate representation of modules."""

from __future__ import annotations

from typing import Dict

from mypyc.common import JsonDict
from mypyc.ir.class_ir import ClassIR
from mypyc.ir.func_ir import FuncDecl, FuncIR
from mypyc.ir.ops import DeserMaps
from mypyc.ir.rtypes import RType, deserialize_type


class ModuleIR:
    """Intermediate representation of a module."""

    def __init__(
        self,
        fullname: str,
        imports: list[str],
        functions: list[FuncIR],
        classes: list[ClassIR],
        final_names: list[tuple[str, RType]],
    ) -> None:
        self.fullname = fullname
        self.imports = imports.copy()
        self.functions = functions
        self.classes = classes
        self.final_names = final_names

    def serialize(self) -> JsonDict:
        return {
            "fullname": self.fullname,
            "imports": self.imports,
            "functions": [f.serialize() for f in self.functions],
            "classes": [c.serialize() for c in self.classes],
            "final_names": [(k, t.serialize()) for k, t in self.final_names],
        }

    @classmethod
    def deserialize(cls, data: JsonDict, ctx: DeserMaps) -> ModuleIR:
        return ModuleIR(
            data["fullname"],
            data["imports"],
            [ctx.functions[FuncDecl.get_id_from_json(f)] for f in data["functions"]],
            [ClassIR.deserialize(c, ctx) for c in data["classes"]],
            [(k, deserialize_type(t, ctx)) for k, t in data["final_names"]],
        )


def deserialize_modules(
    data: dict[str, JsonDict], ctx: DeserMaps
) -> dict[str, ModuleIR]:
    """Deserialize a collection of modules.

    The modules can contain dependencies on each other.

    Arguments:
        data: A dict containing the modules to deserialize.
        ctx: The deserialization maps to use and to populate.
             They are populated with information from the deserialized
             modules and as a precondition must have been populated by
             deserializing any dependencies of the modules being deserialized
             (outside of dependencies between the modules themselves).

    Returns a map containing the deserialized modules.
    """
    for mod in data.values():
        # First create ClassIRs for every class so that we can construct types and whatnot
        for cls in mod["classes"]:
            ir = ClassIR(cls["name"], cls["module_name"])
            assert ir.fullname not in ctx.classes, (
                "Class %s already in map" % ir.fullname
            )
            ctx.classes[ir.fullname] = ir

    for mod in data.values():
        # Then deserialize all of the functions so that methods are available
        # to the class deserialization.
        for method in mod["functions"]:
            func = FuncIR.deserialize(method, ctx)
            assert func.decl.id not in ctx.functions, (
                "Method %s already in map" % func.decl.fullname
            )
            ctx.functions[func.decl.id] = func

    return {k: ModuleIR.deserialize(v, ctx) for k, v in data.items()}


# ModulesIRs should also always be an *OrderedDict*, but if we
# declared it that way we would need to put it in quotes everywhere...
ModuleIRs = Dict[str, ModuleIR]
