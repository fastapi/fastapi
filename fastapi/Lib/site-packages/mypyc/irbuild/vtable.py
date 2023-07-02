"""Compute vtables of native (extension) classes."""

from __future__ import annotations

import itertools

from mypyc.ir.class_ir import ClassIR, VTableEntries, VTableMethod
from mypyc.sametype import is_same_method_signature


def compute_vtable(cls: ClassIR) -> None:
    """Compute the vtable structure for a class."""
    if cls.vtable is not None:
        return

    if not cls.is_generated:
        cls.has_dict = any(x.inherits_python for x in cls.mro)

    for t in cls.mro[1:]:
        # Make sure all ancestors are processed first
        compute_vtable(t)
        # Merge attributes from traits into the class
        if not t.is_trait:
            continue
        for name, typ in t.attributes.items():
            if not cls.is_trait and not any(name in b.attributes for b in cls.base_mro):
                cls.attributes[name] = typ

    cls.vtable = {}
    if cls.base:
        assert cls.base.vtable is not None
        cls.vtable.update(cls.base.vtable)
        cls.vtable_entries = specialize_parent_vtable(cls, cls.base)

    # Include the vtable from the parent classes, but handle method overrides.
    entries = cls.vtable_entries

    all_traits = [t for t in cls.mro if t.is_trait]

    for t in [cls] + cls.traits:
        for fn in itertools.chain(t.methods.values()):
            # TODO: don't generate a new entry when we overload without changing the type
            if fn == cls.get_method(fn.name, prefer_method=True):
                cls.vtable[fn.name] = len(entries)
                # If the class contains a glue method referring to itself, that is a
                # shadow glue method to support interpreted subclasses.
                shadow = cls.glue_methods.get((cls, fn.name))
                entries.append(VTableMethod(t, fn.name, fn, shadow))

    # Compute vtables for all of the traits that the class implements
    if not cls.is_trait:
        for trait in all_traits:
            compute_vtable(trait)
            cls.trait_vtables[trait] = specialize_parent_vtable(cls, trait)


def specialize_parent_vtable(cls: ClassIR, parent: ClassIR) -> VTableEntries:
    """Generate the part of a vtable corresponding to a parent class or trait"""
    updated = []
    for entry in parent.vtable_entries:
        # Find the original method corresponding to this vtable entry.
        # (This may not be the method in the entry, if it was overridden.)
        orig_parent_method = entry.cls.get_method(entry.name, prefer_method=True)
        assert orig_parent_method
        method_cls = cls.get_method_and_class(entry.name, prefer_method=True)
        if method_cls:
            child_method, defining_cls = method_cls
            # TODO: emit a wrapper for __init__ that raises or something
            if (
                is_same_method_signature(orig_parent_method.sig, child_method.sig)
                or orig_parent_method.name == "__init__"
            ):
                entry = VTableMethod(
                    entry.cls, entry.name, child_method, entry.shadow_method
                )
            else:
                entry = VTableMethod(
                    entry.cls,
                    entry.name,
                    defining_cls.glue_methods[(entry.cls, entry.name)],
                    entry.shadow_method,
                )
        updated.append(entry)
    return updated
