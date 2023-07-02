from __future__ import annotations

from typing import Callable

from mypy.nodes import TypeInfo
from mypy.types import Instance
from mypy.typestate import type_state


def calculate_mro(
    info: TypeInfo, obj_type: Callable[[], Instance] | None = None
) -> None:
    """Calculate and set mro (method resolution order).

    Raise MroError if cannot determine mro.
    """
    mro = linearize_hierarchy(info, obj_type)
    assert mro, f"Could not produce a MRO at all for {info}"
    info.mro = mro
    # The property of falling back to Any is inherited.
    info.fallback_to_any = any(baseinfo.fallback_to_any for baseinfo in info.mro)
    type_state.reset_all_subtype_caches_for(info)


class MroError(Exception):
    """Raised if a consistent mro cannot be determined for a class."""


def linearize_hierarchy(
    info: TypeInfo, obj_type: Callable[[], Instance] | None = None
) -> list[TypeInfo]:
    # TODO describe
    if info.mro:
        return info.mro
    bases = info.direct_base_classes()
    if not bases and info.fullname != "builtins.object" and obj_type is not None:
        # Probably an error, add a dummy `object` base class,
        # otherwise MRO calculation may spuriously fail.
        bases = [obj_type().type]
    lin_bases = []
    for base in bases:
        assert base is not None, f"Cannot linearize bases for {info.fullname} {bases}"
        lin_bases.append(linearize_hierarchy(base, obj_type))
    lin_bases.append(bases)
    return [info] + merge(lin_bases)


def merge(seqs: list[list[TypeInfo]]) -> list[TypeInfo]:
    seqs = [s.copy() for s in seqs]
    result: list[TypeInfo] = []
    while True:
        seqs = [s for s in seqs if s]
        if not seqs:
            return result
        for seq in seqs:
            head = seq[0]
            if not [s for s in seqs if head in s[1:]]:
                break
        else:
            raise MroError()
        result.append(head)
        for s in seqs:
            if s[0] is head:
                del s[0]
