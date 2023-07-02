"""
This is a module for various lookup functions:
functions that will find a semantic node by its name.
"""

from __future__ import annotations

from mypy.nodes import MypyFile, SymbolTableNode, TypeInfo

# TODO: gradually move existing lookup functions to this module.


def lookup_fully_qualified(
    name: str, modules: dict[str, MypyFile], *, raise_on_missing: bool = False
) -> SymbolTableNode | None:
    """Find a symbol using it fully qualified name.

    The algorithm has two steps: first we try splitting the name on '.' to find
    the module, then iteratively look for each next chunk after a '.' (e.g. for
    nested classes).

    This function should *not* be used to find a module. Those should be looked
    in the modules dictionary.
    """
    head = name
    rest = []
    # 1. Find a module tree in modules dictionary.
    while True:
        if "." not in head:
            if raise_on_missing:
                assert "." in head, f"Cannot find module for {name}"
            return None
        head, tail = head.rsplit(".", maxsplit=1)
        rest.append(tail)
        mod = modules.get(head)
        if mod is not None:
            break
    names = mod.names
    # 2. Find the symbol in the module tree.
    if not rest:
        # Looks like a module, don't use this to avoid confusions.
        if raise_on_missing:
            assert rest, f"Cannot find {name}, got a module symbol"
        return None
    while True:
        key = rest.pop()
        if key not in names:
            if raise_on_missing:
                assert key in names, f"Cannot find component {key!r} for {name!r}"
            return None
        stnode = names[key]
        if not rest:
            return stnode
        node = stnode.node
        # In fine-grained mode, could be a cross-reference to a deleted module
        # or a Var made up for a missing module.
        if not isinstance(node, TypeInfo):
            if raise_on_missing:
                assert node, f"Cannot find {name}"
            return None
        names = node.names
