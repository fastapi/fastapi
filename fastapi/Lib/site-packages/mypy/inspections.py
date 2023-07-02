from __future__ import annotations

import os
from collections import defaultdict
from functools import cmp_to_key
from typing import Callable

from mypy.build import State
from mypy.find_sources import InvalidSourceList, SourceFinder
from mypy.messages import format_type
from mypy.modulefinder import PYTHON_EXTENSIONS
from mypy.nodes import (
    LDEF,
    Decorator,
    Expression,
    FuncBase,
    MemberExpr,
    MypyFile,
    Node,
    OverloadedFuncDef,
    RefExpr,
    SymbolNode,
    TypeInfo,
    Var,
)
from mypy.server.update import FineGrainedBuildManager
from mypy.traverser import ExtendedTraverserVisitor
from mypy.typeops import tuple_fallback
from mypy.types import (
    FunctionLike,
    Instance,
    LiteralType,
    ProperType,
    TupleType,
    TypedDictType,
    TypeVarType,
    UnionType,
    get_proper_type,
)
from mypy.typevars import fill_typevars_with_any


def node_starts_after(o: Node, line: int, column: int) -> bool:
    return o.line > line or o.line == line and o.column > column


def node_ends_before(o: Node, line: int, column: int) -> bool:
    # Unfortunately, end positions for some statements are a mess,
    # e.g. overloaded functions, so we return False when we don't know.
    if o.end_line is not None and o.end_column is not None:
        if o.end_line < line or o.end_line == line and o.end_column < column:
            return True
    return False


def expr_span(expr: Expression) -> str:
    """Format expression span as in mypy error messages."""
    return f"{expr.line}:{expr.column + 1}:{expr.end_line}:{expr.end_column}"


def get_instance_fallback(typ: ProperType) -> list[Instance]:
    """Returns the Instance fallback for this type if one exists or None."""
    if isinstance(typ, Instance):
        return [typ]
    elif isinstance(typ, TupleType):
        return [tuple_fallback(typ)]
    elif isinstance(typ, TypedDictType):
        return [typ.fallback]
    elif isinstance(typ, FunctionLike):
        return [typ.fallback]
    elif isinstance(typ, LiteralType):
        return [typ.fallback]
    elif isinstance(typ, TypeVarType):
        if typ.values:
            res = []
            for t in typ.values:
                res.extend(get_instance_fallback(get_proper_type(t)))
            return res
        return get_instance_fallback(get_proper_type(typ.upper_bound))
    elif isinstance(typ, UnionType):
        res = []
        for t in typ.items:
            res.extend(get_instance_fallback(get_proper_type(t)))
        return res
    return []


def find_node(name: str, info: TypeInfo) -> Var | FuncBase | None:
    """Find the node defining member 'name' in given TypeInfo."""
    # TODO: this code shares some logic with checkmember.py
    method = info.get_method(name)
    if method:
        if isinstance(method, Decorator):
            return method.var
        if method.is_property:
            assert isinstance(method, OverloadedFuncDef)
            dec = method.items[0]
            assert isinstance(dec, Decorator)
            return dec.var
        return method
    else:
        # don't have such method, maybe variable?
        node = info.get(name)
        v = node.node if node else None
        if isinstance(v, Var):
            return v
    return None


def find_module_by_fullname(fullname: str, modules: dict[str, State]) -> State | None:
    """Find module by a node fullname.

    This logic mimics the one we use in fixup, so should be good enough.
    """
    head = fullname
    # Special case: a module symbol is considered to be defined in itself, not in enclosing
    # package, since this is what users want when clicking go to definition on a module.
    if head in modules:
        return modules[head]
    while True:
        if "." not in head:
            return None
        head, tail = head.rsplit(".", maxsplit=1)
        mod = modules.get(head)
        if mod is not None:
            return mod


class SearchVisitor(ExtendedTraverserVisitor):
    """Visitor looking for an expression whose span matches given one exactly."""

    def __init__(self, line: int, column: int, end_line: int, end_column: int) -> None:
        self.line = line
        self.column = column
        self.end_line = end_line
        self.end_column = end_column
        self.result: Expression | None = None

    def visit(self, o: Node) -> bool:
        if node_starts_after(o, self.line, self.column):
            return False
        if node_ends_before(o, self.end_line, self.end_column):
            return False
        if (
            o.line == self.line
            and o.end_line == self.end_line
            and o.column == self.column
            and o.end_column == self.end_column
        ):
            if isinstance(o, Expression):
                self.result = o
        return self.result is None


def find_by_location(
    tree: MypyFile, line: int, column: int, end_line: int, end_column: int
) -> Expression | None:
    """Find an expression matching given span, or None if not found."""
    if end_line < line:
        raise ValueError('"end_line" must not be before "line"')
    if end_line == line and end_column <= column:
        raise ValueError('"end_column" must be after "column"')
    visitor = SearchVisitor(line, column, end_line, end_column)
    tree.accept(visitor)
    return visitor.result


class SearchAllVisitor(ExtendedTraverserVisitor):
    """Visitor looking for all expressions whose spans enclose given position."""

    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column
        self.result: list[Expression] = []

    def visit(self, o: Node) -> bool:
        if node_starts_after(o, self.line, self.column):
            return False
        if node_ends_before(o, self.line, self.column):
            return False
        if isinstance(o, Expression):
            self.result.append(o)
        return True


def find_all_by_location(tree: MypyFile, line: int, column: int) -> list[Expression]:
    """Find all expressions enclosing given position starting from innermost."""
    visitor = SearchAllVisitor(line, column)
    tree.accept(visitor)
    return list(reversed(visitor.result))


class InspectionEngine:
    """Engine for locating and statically inspecting expressions."""

    def __init__(
        self,
        fg_manager: FineGrainedBuildManager,
        *,
        verbosity: int = 0,
        limit: int = 0,
        include_span: bool = False,
        include_kind: bool = False,
        include_object_attrs: bool = False,
        union_attrs: bool = False,
        force_reload: bool = False,
    ) -> None:
        self.fg_manager = fg_manager
        self.finder = SourceFinder(
            self.fg_manager.manager.fscache, self.fg_manager.manager.options
        )
        self.verbosity = verbosity
        self.limit = limit
        self.include_span = include_span
        self.include_kind = include_kind
        self.include_object_attrs = include_object_attrs
        self.union_attrs = union_attrs
        self.force_reload = force_reload
        # Module for which inspection was requested.
        self.module: State | None = None

    def parse_location(self, location: str) -> tuple[str, list[int]]:
        if location.count(":") not in [2, 4]:
            raise ValueError("Format should be file:line:column[:end_line:end_column]")
        parts = location.split(":")
        module, *rest = parts
        return module, [int(p) for p in rest]

    def reload_module(self, state: State) -> None:
        """Reload given module while temporary exporting types."""
        old = self.fg_manager.manager.options.export_types
        self.fg_manager.manager.options.export_types = True
        try:
            self.fg_manager.flush_cache()
            assert state.path is not None
            self.fg_manager.update([(state.id, state.path)], [])
        finally:
            self.fg_manager.manager.options.export_types = old

    def expr_type(self, expression: Expression) -> tuple[str, bool]:
        """Format type for an expression using current options.

        If type is known, second item returned is True. If type is not known, an error
        message is returned instead, and second item returned is False.
        """
        expr_type = self.fg_manager.manager.all_types.get(expression)
        if expr_type is None:
            return self.missing_type(expression), False

        type_str = format_type(
            expr_type, self.fg_manager.manager.options, verbosity=self.verbosity
        )
        return self.add_prefixes(type_str, expression), True

    def object_type(self) -> Instance:
        builtins = self.fg_manager.graph["builtins"].tree
        assert builtins is not None
        object_node = builtins.names["object"].node
        assert isinstance(object_node, TypeInfo)
        return Instance(object_node, [])

    def collect_attrs(self, instances: list[Instance]) -> dict[TypeInfo, list[str]]:
        """Collect attributes from all union/typevar variants."""

        def item_attrs(attr_dict: dict[TypeInfo, list[str]]) -> set[str]:
            attrs = set()
            for base in attr_dict:
                attrs |= set(attr_dict[base])
            return attrs

        def cmp_types(x: TypeInfo, y: TypeInfo) -> int:
            if x in y.mro:
                return 1
            if y in x.mro:
                return -1
            return 0

        # First gather all attributes for every union variant.
        assert instances
        all_attrs = []
        for instance in instances:
            attrs = {}
            mro = instance.type.mro
            if not self.include_object_attrs:
                mro = mro[:-1]
            for base in mro:
                attrs[base] = sorted(base.names)
            all_attrs.append(attrs)

        # Find attributes valid for all variants in a union or type variable.
        intersection = item_attrs(all_attrs[0])
        for item in all_attrs[1:]:
            intersection &= item_attrs(item)

        # Combine attributes from all variants into a single dict while
        # also removing invalid attributes (unless using --union-attrs).
        combined_attrs = defaultdict(list)
        for item in all_attrs:
            for base in item:
                if base in combined_attrs:
                    continue
                for name in item[base]:
                    if self.union_attrs or name in intersection:
                        combined_attrs[base].append(name)

        # Sort bases by MRO, unrelated will appear in the order they appeared as union variants.
        sorted_bases = sorted(combined_attrs.keys(), key=cmp_to_key(cmp_types))
        result = {}
        for base in sorted_bases:
            if not combined_attrs[base]:
                # Skip bases where everytihng was filtered out.
                continue
            result[base] = combined_attrs[base]
        return result

    def _fill_from_dict(
        self, attrs_strs: list[str], attrs_dict: dict[TypeInfo, list[str]]
    ) -> None:
        for base in attrs_dict:
            cls_name = base.name if self.verbosity < 1 else base.fullname
            attrs = [f'"{attr}"' for attr in attrs_dict[base]]
            attrs_strs.append(f'"{cls_name}": [{", ".join(attrs)}]')

    def expr_attrs(self, expression: Expression) -> tuple[str, bool]:
        """Format attributes that are valid for a given expression.

        If expression type is not an Instance, try using fallback. Attributes are
        returned as a JSON (ordered by MRO) that maps base class name to list of
        attributes. Attributes may appear in multiple bases if overridden (we simply
        follow usual mypy logic for creating new Vars etc).
        """
        expr_type = self.fg_manager.manager.all_types.get(expression)
        if expr_type is None:
            return self.missing_type(expression), False

        expr_type = get_proper_type(expr_type)
        instances = get_instance_fallback(expr_type)
        if not instances:
            # Everything is an object in Python.
            instances = [self.object_type()]

        attrs_dict = self.collect_attrs(instances)

        # Special case: modules have names apart from those from ModuleType.
        if isinstance(expression, RefExpr) and isinstance(expression.node, MypyFile):
            node = expression.node
            names = sorted(node.names)
            if "__builtins__" in names:
                # This is just to make tests stable. No one will really need ths name.
                names.remove("__builtins__")
            mod_dict = {f'"<{node.fullname}>"': [f'"{name}"' for name in names]}
        else:
            mod_dict = {}

        # Special case: for class callables, prepend with the class attributes.
        # TODO: also handle cases when such callable appears in a union.
        if isinstance(expr_type, FunctionLike) and expr_type.is_type_obj():
            template = fill_typevars_with_any(expr_type.type_object())
            class_dict = self.collect_attrs(get_instance_fallback(template))
        else:
            class_dict = {}

        # We don't use JSON dump to be sure keys order is always preserved.
        base_attrs = []
        if mod_dict:
            for mod in mod_dict:
                base_attrs.append(f'{mod}: [{", ".join(mod_dict[mod])}]')
        self._fill_from_dict(base_attrs, class_dict)
        self._fill_from_dict(base_attrs, attrs_dict)
        return self.add_prefixes(f'{{{", ".join(base_attrs)}}}', expression), True

    def format_node(self, module: State, node: FuncBase | SymbolNode) -> str:
        return f"{module.path}:{node.line}:{node.column + 1}:{node.name}"

    def collect_nodes(self, expression: RefExpr) -> list[FuncBase | SymbolNode]:
        """Collect nodes that can be referred to by an expression.

        Note: it can be more than one for example in case of a union attribute.
        """
        node: FuncBase | SymbolNode | None = expression.node
        nodes: list[FuncBase | SymbolNode]
        if node is None:
            # Tricky case: instance attribute
            if isinstance(expression, MemberExpr) and expression.kind is None:
                base_type = self.fg_manager.manager.all_types.get(expression.expr)
                if base_type is None:
                    return []

                # Now we use the base type to figure out where the attribute is defined.
                base_type = get_proper_type(base_type)
                instances = get_instance_fallback(base_type)
                nodes = []
                for instance in instances:
                    node = find_node(expression.name, instance.type)
                    if node:
                        nodes.append(node)
                if not nodes:
                    # Try checking class namespace if attribute is on a class object.
                    if isinstance(base_type, FunctionLike) and base_type.is_type_obj():
                        instances = get_instance_fallback(
                            fill_typevars_with_any(base_type.type_object())
                        )
                        for instance in instances:
                            node = find_node(expression.name, instance.type)
                            if node:
                                nodes.append(node)
                    else:
                        # Still no luck, give up.
                        return []
            else:
                return []
        else:
            # Easy case: a module-level definition
            nodes = [node]
        return nodes

    def modules_for_nodes(
        self, nodes: list[FuncBase | SymbolNode], expression: RefExpr
    ) -> tuple[dict[FuncBase | SymbolNode, State], bool]:
        """Gather modules where given nodes where defined.

        Also check if they need to be refreshed (cached nodes may have
        lines/columns missing).
        """
        modules = {}
        reload_needed = False
        for node in nodes:
            module = find_module_by_fullname(node.fullname, self.fg_manager.graph)
            if not module:
                if expression.kind == LDEF and self.module:
                    module = self.module
                else:
                    continue
            modules[node] = module
            if not module.tree or module.tree.is_cache_skeleton or self.force_reload:
                reload_needed |= not module.tree or module.tree.is_cache_skeleton
                self.reload_module(module)
        return modules, reload_needed

    def expression_def(self, expression: Expression) -> tuple[str, bool]:
        """Find and format definition location for an expression.

        If it is not a RefExpr, it is effectively skipped by returning an
        empty result.
        """
        if not isinstance(expression, RefExpr):
            # If there are no suitable matches at all, we return error later.
            return "", True

        nodes = self.collect_nodes(expression)

        if not nodes:
            return self.missing_node(expression), False

        modules, reload_needed = self.modules_for_nodes(nodes, expression)
        if reload_needed:
            # TODO: line/column are not stored in cache for vast majority of symbol nodes.
            # Adding them will make thing faster, but will have visible memory impact.
            nodes = self.collect_nodes(expression)
            modules, reload_needed = self.modules_for_nodes(nodes, expression)
            assert not reload_needed

        result = []
        for node in modules:
            result.append(self.format_node(modules[node], node))

        if not result:
            return self.missing_node(expression), False

        return self.add_prefixes(", ".join(result), expression), True

    def missing_type(self, expression: Expression) -> str:
        alt_suggestion = ""
        if not self.force_reload:
            alt_suggestion = " or try --force-reload"
        return (
            f'No known type available for "{type(expression).__name__}"'
            f" (maybe unreachable{alt_suggestion})"
        )

    def missing_node(self, expression: Expression) -> str:
        return (
            f'Cannot find definition for "{type(expression).__name__}"'
            f" at {expr_span(expression)}"
        )

    def add_prefixes(self, result: str, expression: Expression) -> str:
        prefixes = []
        if self.include_kind:
            prefixes.append(f"{type(expression).__name__}")
        if self.include_span:
            prefixes.append(expr_span(expression))
        if prefixes:
            prefix = ":".join(prefixes) + " -> "
        else:
            prefix = ""
        return prefix + result

    def run_inspection_by_exact_location(
        self,
        tree: MypyFile,
        line: int,
        column: int,
        end_line: int,
        end_column: int,
        method: Callable[[Expression], tuple[str, bool]],
    ) -> dict[str, object]:
        """Get type of an expression matching a span.

        Type or error is returned as a standard daemon response dict.
        """
        try:
            expression = find_by_location(tree, line, column - 1, end_line, end_column)
        except ValueError as err:
            return {"error": str(err)}

        if expression is None:
            span = f"{line}:{column}:{end_line}:{end_column}"
            return {
                "out": f"Can't find expression at span {span}",
                "err": "",
                "status": 1,
            }

        inspection_str, success = method(expression)
        return {"out": inspection_str, "err": "", "status": 0 if success else 1}

    def run_inspection_by_position(
        self,
        tree: MypyFile,
        line: int,
        column: int,
        method: Callable[[Expression], tuple[str, bool]],
    ) -> dict[str, object]:
        """Get types of all expressions enclosing a position.

        Types and/or errors are returned as a standard daemon response dict.
        """
        expressions = find_all_by_location(tree, line, column - 1)
        if not expressions:
            position = f"{line}:{column}"
            return {
                "out": f"Can't find any expressions at position {position}",
                "err": "",
                "status": 1,
            }

        inspection_strs = []
        status = 0
        for expression in expressions:
            inspection_str, success = method(expression)
            if not success:
                status = 1
            if inspection_str:
                inspection_strs.append(inspection_str)
        if self.limit:
            inspection_strs = inspection_strs[: self.limit]
        return {"out": "\n".join(inspection_strs), "err": "", "status": status}

    def find_module(self, file: str) -> tuple[State | None, dict[str, object]]:
        """Find module by path, or return a suitable error message.

        Note we don't use exceptions to simplify handling 1 vs 2 statuses.
        """
        if not any(file.endswith(ext) for ext in PYTHON_EXTENSIONS):
            return None, {"error": "Source file is not a Python file"}

        try:
            module, _ = self.finder.crawl_up(os.path.normpath(file))
        except InvalidSourceList:
            return None, {"error": "Invalid source file name: " + file}

        state = self.fg_manager.graph.get(module)
        self.module = state
        return (
            state,
            {"out": f"Unknown module: {module}", "err": "", "status": 1}
            if state is None
            else {},
        )

    def run_inspection(
        self, location: str, method: Callable[[Expression], tuple[str, bool]]
    ) -> dict[str, object]:
        """Top-level logic to inspect expression(s) at a location.

        This can be re-used by various simple inspections.
        """
        try:
            file, pos = self.parse_location(location)
        except ValueError as err:
            return {"error": str(err)}

        state, err_dict = self.find_module(file)
        if state is None:
            assert err_dict
            return err_dict

        # Force reloading to load from cache, account for any edits, etc.
        if not state.tree or state.tree.is_cache_skeleton or self.force_reload:
            self.reload_module(state)
        assert state.tree is not None

        if len(pos) == 4:
            # Full span, return an exact match only.
            line, column, end_line, end_column = pos
            return self.run_inspection_by_exact_location(
                state.tree, line, column, end_line, end_column, method
            )
        assert len(pos) == 2
        # Inexact location, return all expressions.
        line, column = pos
        return self.run_inspection_by_position(state.tree, line, column, method)

    def get_type(self, location: str) -> dict[str, object]:
        """Get types of expression(s) at a location."""
        return self.run_inspection(location, self.expr_type)

    def get_attrs(self, location: str) -> dict[str, object]:
        """Get attributes of expression(s) at a location."""
        return self.run_inspection(location, self.expr_attrs)

    def get_definition(self, location: str) -> dict[str, object]:
        """Get symbol definitions of expression(s) at a location."""
        result = self.run_inspection(location, self.expression_def)
        if "out" in result and not result["out"]:
            # None of the expressions found turns out to be a RefExpr.
            _, location = location.split(":", maxsplit=1)
            result["out"] = f"No name or member expressions at {location}"
            result["status"] = 1
        return result
