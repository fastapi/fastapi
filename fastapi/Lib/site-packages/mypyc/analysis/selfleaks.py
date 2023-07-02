from __future__ import annotations

from typing import Set, Tuple

from mypyc.analysis.dataflow import CFG, MAYBE_ANALYSIS, AnalysisResult, run_analysis
from mypyc.ir.ops import (
    Assign,
    AssignMulti,
    BasicBlock,
    Box,
    Branch,
    Call,
    CallC,
    Cast,
    ComparisonOp,
    Extend,
    FloatComparisonOp,
    FloatNeg,
    FloatOp,
    GetAttr,
    GetElementPtr,
    Goto,
    InitStatic,
    IntOp,
    KeepAlive,
    LoadAddress,
    LoadErrorValue,
    LoadGlobal,
    LoadLiteral,
    LoadMem,
    LoadStatic,
    MethodCall,
    OpVisitor,
    RaiseStandardError,
    Register,
    RegisterOp,
    Return,
    SetAttr,
    SetMem,
    Truncate,
    TupleGet,
    TupleSet,
    Unbox,
    Unreachable,
)
from mypyc.ir.rtypes import RInstance

GenAndKill = Tuple[Set[None], Set[None]]

CLEAN: GenAndKill = (set(), set())
DIRTY: GenAndKill = ({None}, {None})


class SelfLeakedVisitor(OpVisitor[GenAndKill]):
    """Analyze whether 'self' may be seen by arbitrary code in '__init__'.

    More formally, the set is not empty if along some path from IR entry point
    arbitrary code could have been executed that has access to 'self'.

    (We don't consider access via 'gc.get_objects()'.)
    """

    def __init__(self, self_reg: Register) -> None:
        self.self_reg = self_reg

    def visit_goto(self, op: Goto) -> GenAndKill:
        return CLEAN

    def visit_branch(self, op: Branch) -> GenAndKill:
        return CLEAN

    def visit_return(self, op: Return) -> GenAndKill:
        # Consider all exits from the function 'dirty' since they implicitly
        # cause 'self' to be returned.
        return DIRTY

    def visit_unreachable(self, op: Unreachable) -> GenAndKill:
        return CLEAN

    def visit_assign(self, op: Assign) -> GenAndKill:
        if op.src is self.self_reg or op.dest is self.self_reg:
            return DIRTY
        return CLEAN

    def visit_assign_multi(self, op: AssignMulti) -> GenAndKill:
        return CLEAN

    def visit_set_mem(self, op: SetMem) -> GenAndKill:
        return CLEAN

    def visit_call(self, op: Call) -> GenAndKill:
        fn = op.fn
        if fn.class_name and fn.name == "__init__":
            self_type = op.fn.sig.args[0].type
            assert isinstance(self_type, RInstance)
            cl = self_type.class_ir
            if not cl.init_self_leak:
                return CLEAN
        return self.check_register_op(op)

    def visit_method_call(self, op: MethodCall) -> GenAndKill:
        return self.check_register_op(op)

    def visit_load_error_value(self, op: LoadErrorValue) -> GenAndKill:
        return CLEAN

    def visit_load_literal(self, op: LoadLiteral) -> GenAndKill:
        return CLEAN

    def visit_get_attr(self, op: GetAttr) -> GenAndKill:
        cl = op.class_type.class_ir
        if cl.get_method(op.attr):
            # Property -- calls a function
            return self.check_register_op(op)
        return CLEAN

    def visit_set_attr(self, op: SetAttr) -> GenAndKill:
        cl = op.class_type.class_ir
        if cl.get_method(op.attr):
            # Property - calls a function
            return self.check_register_op(op)
        return CLEAN

    def visit_load_static(self, op: LoadStatic) -> GenAndKill:
        return CLEAN

    def visit_init_static(self, op: InitStatic) -> GenAndKill:
        return self.check_register_op(op)

    def visit_tuple_get(self, op: TupleGet) -> GenAndKill:
        return CLEAN

    def visit_tuple_set(self, op: TupleSet) -> GenAndKill:
        return self.check_register_op(op)

    def visit_box(self, op: Box) -> GenAndKill:
        return self.check_register_op(op)

    def visit_unbox(self, op: Unbox) -> GenAndKill:
        return self.check_register_op(op)

    def visit_cast(self, op: Cast) -> GenAndKill:
        return self.check_register_op(op)

    def visit_raise_standard_error(self, op: RaiseStandardError) -> GenAndKill:
        return CLEAN

    def visit_call_c(self, op: CallC) -> GenAndKill:
        return self.check_register_op(op)

    def visit_truncate(self, op: Truncate) -> GenAndKill:
        return CLEAN

    def visit_extend(self, op: Extend) -> GenAndKill:
        return CLEAN

    def visit_load_global(self, op: LoadGlobal) -> GenAndKill:
        return CLEAN

    def visit_int_op(self, op: IntOp) -> GenAndKill:
        return CLEAN

    def visit_comparison_op(self, op: ComparisonOp) -> GenAndKill:
        return CLEAN

    def visit_float_op(self, op: FloatOp) -> GenAndKill:
        return CLEAN

    def visit_float_neg(self, op: FloatNeg) -> GenAndKill:
        return CLEAN

    def visit_float_comparison_op(self, op: FloatComparisonOp) -> GenAndKill:
        return CLEAN

    def visit_load_mem(self, op: LoadMem) -> GenAndKill:
        return CLEAN

    def visit_get_element_ptr(self, op: GetElementPtr) -> GenAndKill:
        return CLEAN

    def visit_load_address(self, op: LoadAddress) -> GenAndKill:
        return CLEAN

    def visit_keep_alive(self, op: KeepAlive) -> GenAndKill:
        return CLEAN

    def check_register_op(self, op: RegisterOp) -> GenAndKill:
        if any(src is self.self_reg for src in op.sources()):
            return DIRTY
        return CLEAN


def analyze_self_leaks(
    blocks: list[BasicBlock], self_reg: Register, cfg: CFG
) -> AnalysisResult[None]:
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=SelfLeakedVisitor(self_reg),
        initial=set(),
        backward=False,
        kind=MAYBE_ANALYSIS,
    )
