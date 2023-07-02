"""Transformation for inserting refrecence count inc/dec opcodes.

This transformation happens towards the end of compilation. Before this
transformation, reference count management is not explicitly handled at all.
By postponing this pass, the previous passes are simpler as they don't have
to update reference count opcodes.

The approach is to decrement reference counts soon after a value is no
longer live, to quickly free memory (and call __del__ methods), though
there are no strict guarantees -- other than that local variables are
freed before return from a function.

Function arguments are a little special. They are initially considered
'borrowed' from the caller and their reference counts don't need to be
decremented before returning. An assignment to a borrowed value turns it
into a regular, owned reference that needs to freed before return.
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

from mypyc.analysis.dataflow import (
    AnalysisDict,
    analyze_borrowed_arguments,
    analyze_live_regs,
    analyze_must_defined_regs,
    cleanup_cfg,
    get_cfg,
)
from mypyc.ir.func_ir import FuncIR, all_values
from mypyc.ir.ops import (
    Assign,
    BasicBlock,
    Branch,
    ControlOp,
    DecRef,
    Goto,
    IncRef,
    Integer,
    KeepAlive,
    LoadAddress,
    Op,
    Register,
    RegisterOp,
    Value,
)

Decs = Tuple[Tuple[Value, bool], ...]
Incs = Tuple[Value, ...]

# A cache of basic blocks that decrement and increment specific values
# and then jump to some target block. This lets us cut down on how
# much code we generate in some circumstances.
BlockCache = Dict[Tuple[BasicBlock, Decs, Incs], BasicBlock]


def insert_ref_count_opcodes(ir: FuncIR) -> None:
    """Insert reference count inc/dec opcodes to a function.

    This is the entry point to this module.
    """
    cfg = get_cfg(ir.blocks)
    values = all_values(ir.arg_regs, ir.blocks)

    borrowed = {value for value in values if value.is_borrowed}
    args: set[Value] = set(ir.arg_regs)
    live = analyze_live_regs(ir.blocks, cfg)
    borrow = analyze_borrowed_arguments(ir.blocks, cfg, borrowed)
    defined = analyze_must_defined_regs(
        ir.blocks, cfg, args, values, strict_errors=True
    )
    ordering = make_value_ordering(ir)
    cache: BlockCache = {}
    for block in ir.blocks.copy():
        if isinstance(block.ops[-1], (Branch, Goto)):
            insert_branch_inc_and_decrefs(
                block,
                cache,
                ir.blocks,
                live.before,
                borrow.before,
                borrow.after,
                defined.after,
                ordering,
            )
        transform_block(block, live.before, live.after, borrow.before, defined.after)

    cleanup_cfg(ir.blocks)


def is_maybe_undefined(post_must_defined: set[Value], src: Value) -> bool:
    return isinstance(src, Register) and src not in post_must_defined


def maybe_append_dec_ref(
    ops: list[Op],
    dest: Value,
    defined: AnalysisDict[Value],
    key: tuple[BasicBlock, int],
) -> None:
    if dest.type.is_refcounted and not isinstance(dest, Integer):
        ops.append(DecRef(dest, is_xdec=is_maybe_undefined(defined[key], dest)))


def maybe_append_inc_ref(ops: list[Op], dest: Value) -> None:
    if dest.type.is_refcounted:
        ops.append(IncRef(dest))


def transform_block(
    block: BasicBlock,
    pre_live: AnalysisDict[Value],
    post_live: AnalysisDict[Value],
    pre_borrow: AnalysisDict[Value],
    post_must_defined: AnalysisDict[Value],
) -> None:
    old_ops = block.ops
    ops: list[Op] = []
    for i, op in enumerate(old_ops):
        key = (block, i)

        assert op not in pre_live[key]
        dest = op.dest if isinstance(op, Assign) else op
        stolen = op.stolen()

        # Incref any references that are being stolen that stay live, were borrowed,
        # or are stolen more than once by this operation.
        for j, src in enumerate(stolen):
            if src in post_live[key] or src in pre_borrow[key] or src in stolen[:j]:
                maybe_append_inc_ref(ops, src)
                # For assignments to registers that were already live,
                # decref the old value.
                if dest not in pre_borrow[key] and dest in pre_live[key]:
                    assert isinstance(op, Assign)
                    maybe_append_dec_ref(ops, dest, post_must_defined, key)

        # Strip KeepAlive. Its only purpose is to help with this transform.
        if not isinstance(op, KeepAlive):
            ops.append(op)

        # Control ops don't have any space to insert ops after them, so
        # their inc/decrefs get inserted by insert_branch_inc_and_decrefs.
        if isinstance(op, ControlOp):
            continue

        for src in op.unique_sources():
            # Decrement source that won't be live afterwards.
            if (
                src not in post_live[key]
                and src not in pre_borrow[key]
                and src not in stolen
            ):
                maybe_append_dec_ref(ops, src, post_must_defined, key)
        # Decrement the destination if it is dead after the op and
        # wasn't a borrowed RegisterOp
        if (
            not dest.is_void
            and dest not in post_live[key]
            and not (isinstance(op, RegisterOp) and dest.is_borrowed)
        ):
            maybe_append_dec_ref(ops, dest, post_must_defined, key)
    block.ops = ops


def insert_branch_inc_and_decrefs(
    block: BasicBlock,
    cache: BlockCache,
    blocks: list[BasicBlock],
    pre_live: AnalysisDict[Value],
    pre_borrow: AnalysisDict[Value],
    post_borrow: AnalysisDict[Value],
    post_must_defined: AnalysisDict[Value],
    ordering: dict[Value, int],
) -> None:
    """Insert inc_refs and/or dec_refs after a branch/goto.

    Add dec_refs for registers that become dead after a branch.
    Add inc_refs for registers that become unborrowed after a branch or goto.

    Branches are special as the true and false targets may have a different
    live and borrowed register sets. Add new blocks before the true/false target
    blocks that tweak reference counts.

    Example where we need to add an inc_ref:

      def f(a: int) -> None
          if a:
              a = 1
          return a  # a is borrowed if condition is false and unborrowed if true
    """
    prev_key = (block, len(block.ops) - 1)
    source_live_regs = pre_live[prev_key]
    source_borrowed = post_borrow[prev_key]
    source_defined = post_must_defined[prev_key]

    term = block.terminator
    for i, target in enumerate(term.targets()):
        # HAX: After we've checked against an error value the value we must not touch the
        #      refcount since it will be a null pointer. The correct way to do this would be
        #      to perform data flow analysis on whether a value can be null (or is always
        #      null).
        omitted: Iterable[Value]
        if isinstance(term, Branch) and term.op == Branch.IS_ERROR and i == 0:
            omitted = (term.value,)
        else:
            omitted = ()

        decs = after_branch_decrefs(
            target,
            pre_live,
            source_defined,
            source_borrowed,
            source_live_regs,
            ordering,
            omitted,
        )
        incs = after_branch_increfs(
            target, pre_live, pre_borrow, source_borrowed, ordering
        )
        term.set_target(i, add_block(decs, incs, cache, blocks, target))


def after_branch_decrefs(
    label: BasicBlock,
    pre_live: AnalysisDict[Value],
    source_defined: set[Value],
    source_borrowed: set[Value],
    source_live_regs: set[Value],
    ordering: dict[Value, int],
    omitted: Iterable[Value],
) -> tuple[tuple[Value, bool], ...]:
    target_pre_live = pre_live[label, 0]
    decref = source_live_regs - target_pre_live - source_borrowed
    if decref:
        return tuple(
            (reg, is_maybe_undefined(source_defined, reg))
            for reg in sorted(decref, key=lambda r: ordering[r])
            if reg.type.is_refcounted and reg not in omitted
        )
    return ()


def after_branch_increfs(
    label: BasicBlock,
    pre_live: AnalysisDict[Value],
    pre_borrow: AnalysisDict[Value],
    source_borrowed: set[Value],
    ordering: dict[Value, int],
) -> tuple[Value, ...]:
    target_pre_live = pre_live[label, 0]
    target_borrowed = pre_borrow[label, 0]
    incref = (source_borrowed - target_borrowed) & target_pre_live
    if incref:
        return tuple(
            reg
            for reg in sorted(incref, key=lambda r: ordering[r])
            if reg.type.is_refcounted
        )
    return ()


def add_block(
    decs: Decs,
    incs: Incs,
    cache: BlockCache,
    blocks: list[BasicBlock],
    label: BasicBlock,
) -> BasicBlock:
    if not decs and not incs:
        return label

    # TODO: be able to share *partial* results
    if (label, decs, incs) in cache:
        return cache[label, decs, incs]

    block = BasicBlock()
    blocks.append(block)
    block.ops.extend(DecRef(reg, is_xdec=xdec) for reg, xdec in decs)
    block.ops.extend(IncRef(reg) for reg in incs)
    block.ops.append(Goto(label))
    cache[label, decs, incs] = block
    return block


def make_value_ordering(ir: FuncIR) -> dict[Value, int]:
    """Create a ordering of values that allows them to be sorted.

    This omits registers that are only ever read.
    """
    # TODO: Never initialized values??
    result: dict[Value, int] = {}
    n = 0

    for arg in ir.arg_regs:
        result[arg] = n
        n += 1

    for block in ir.blocks:
        for op in block.ops:
            if (
                isinstance(op, LoadAddress)
                and isinstance(op.src, Register)
                and op.src not in result
            ):
                # Taking the address of a register allows initialization.
                result[op.src] = n
                n += 1
            if isinstance(op, Assign):
                if op.dest not in result:
                    result[op.dest] = n
                    n += 1
            elif op not in result:
                result[op] = n
                n += 1

    return result
