"""Insert checks for uninitialized values."""

from __future__ import annotations

from mypyc.analysis.dataflow import (
    AnalysisDict,
    analyze_must_defined_regs,
    cleanup_cfg,
    get_cfg,
)
from mypyc.common import BITMAP_BITS
from mypyc.ir.func_ir import FuncIR, all_values
from mypyc.ir.ops import (
    Assign,
    BasicBlock,
    Branch,
    ComparisonOp,
    Integer,
    IntOp,
    LoadAddress,
    LoadErrorValue,
    Op,
    RaiseStandardError,
    Register,
    Unreachable,
    Value,
)
from mypyc.ir.rtypes import bitmap_rprimitive


def insert_uninit_checks(ir: FuncIR) -> None:
    # Remove dead blocks from the CFG, which helps avoid spurious
    # checks due to unused error handling blocks.
    cleanup_cfg(ir.blocks)

    cfg = get_cfg(ir.blocks)
    must_defined = analyze_must_defined_regs(
        ir.blocks, cfg, set(ir.arg_regs), all_values(ir.arg_regs, ir.blocks)
    )

    ir.blocks = split_blocks_at_uninits(ir.blocks, must_defined.before)


def split_blocks_at_uninits(
    blocks: list[BasicBlock], pre_must_defined: AnalysisDict[Value]
) -> list[BasicBlock]:
    new_blocks: list[BasicBlock] = []

    init_registers = []
    init_registers_set = set()
    bitmap_registers: list[Register] = []  # Init status bitmaps
    bitmap_backed: list[Register] = []  # These use bitmaps to track init status

    # First split blocks on ops that may raise.
    for block in blocks:
        ops = block.ops
        block.ops = []
        cur_block = block
        new_blocks.append(cur_block)

        for i, op in enumerate(ops):
            defined = pre_must_defined[block, i]
            for src in op.unique_sources():
                # If a register operand is not guaranteed to be
                # initialized is an operand to something other than a
                # check that it is defined, insert a check.

                # Note that for register operand in a LoadAddress op,
                # we should be able to use it without initialization
                # as we may need to use its address to update itself
                if (
                    isinstance(src, Register)
                    and src not in defined
                    and not (isinstance(op, Branch) and op.op == Branch.IS_ERROR)
                    and not isinstance(op, LoadAddress)
                ):
                    new_block, error_block = BasicBlock(), BasicBlock()
                    new_block.error_handler = (
                        error_block.error_handler
                    ) = cur_block.error_handler
                    new_blocks += [error_block, new_block]

                    if src not in init_registers_set:
                        init_registers.append(src)
                        init_registers_set.add(src)

                    if not src.type.error_overlap:
                        cur_block.ops.append(
                            Branch(
                                src,
                                true_label=error_block,
                                false_label=new_block,
                                op=Branch.IS_ERROR,
                                line=op.line,
                            )
                        )
                    else:
                        # We need to use bitmap for this one.
                        check_for_uninit_using_bitmap(
                            cur_block.ops,
                            src,
                            bitmap_registers,
                            bitmap_backed,
                            error_block,
                            new_block,
                            op.line,
                        )

                    raise_std = RaiseStandardError(
                        RaiseStandardError.UNBOUND_LOCAL_ERROR,
                        f'local variable "{src.name}" referenced before assignment',
                        op.line,
                    )
                    error_block.ops.append(raise_std)
                    error_block.ops.append(Unreachable())
                    cur_block = new_block
            cur_block.ops.append(op)

    if bitmap_backed:
        update_register_assignments_to_set_bitmap(
            new_blocks, bitmap_registers, bitmap_backed
        )

    if init_registers:
        new_ops: list[Op] = []
        for reg in init_registers:
            err = LoadErrorValue(reg.type, undefines=True)
            new_ops.append(err)
            new_ops.append(Assign(reg, err))
        for reg in bitmap_registers:
            new_ops.append(Assign(reg, Integer(0, bitmap_rprimitive)))
        new_blocks[0].ops[0:0] = new_ops

    return new_blocks


def check_for_uninit_using_bitmap(
    ops: list[Op],
    src: Register,
    bitmap_registers: list[Register],
    bitmap_backed: list[Register],
    error_block: BasicBlock,
    ok_block: BasicBlock,
    line: int,
) -> None:
    """Check if src is defined using a bitmap.

    Modifies ops, bitmap_registers and bitmap_backed.
    """
    if src not in bitmap_backed:
        # Set up a new bitmap backed register.
        bitmap_backed.append(src)
        n = (len(bitmap_backed) - 1) // BITMAP_BITS
        if len(bitmap_registers) <= n:
            bitmap_registers.append(Register(bitmap_rprimitive, f"__locals_bitmap{n}"))

    index = bitmap_backed.index(src)
    masked = IntOp(
        bitmap_rprimitive,
        bitmap_registers[index // BITMAP_BITS],
        Integer(1 << (index & (BITMAP_BITS - 1)), bitmap_rprimitive),
        IntOp.AND,
        line,
    )
    ops.append(masked)
    chk = ComparisonOp(masked, Integer(0, bitmap_rprimitive), ComparisonOp.EQ)
    ops.append(chk)
    ops.append(Branch(chk, error_block, ok_block, Branch.BOOL))


def update_register_assignments_to_set_bitmap(
    blocks: list[BasicBlock],
    bitmap_registers: list[Register],
    bitmap_backed: list[Register],
) -> None:
    """Update some assignments to registers to also set a bit in a bitmap.

    The bitmaps are used to track if a local variable has been assigned to.

    Modifies blocks.
    """
    for block in blocks:
        if any(isinstance(op, Assign) and op.dest in bitmap_backed for op in block.ops):
            new_ops: list[Op] = []
            for op in block.ops:
                if isinstance(op, Assign) and op.dest in bitmap_backed:
                    index = bitmap_backed.index(op.dest)
                    new_ops.append(op)
                    reg = bitmap_registers[index // BITMAP_BITS]
                    new = IntOp(
                        bitmap_rprimitive,
                        reg,
                        Integer(1 << (index & (BITMAP_BITS - 1)), bitmap_rprimitive),
                        IntOp.OR,
                        op.line,
                    )
                    new_ops.append(new)
                    new_ops.append(Assign(reg, new))
                else:
                    new_ops.append(op)
            block.ops = new_ops
