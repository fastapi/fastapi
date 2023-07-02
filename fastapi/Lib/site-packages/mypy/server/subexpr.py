"""Find all subexpressions of an AST node."""

from __future__ import annotations

from mypy.nodes import (
    AssertTypeExpr,
    AssignmentExpr,
    AwaitExpr,
    CallExpr,
    CastExpr,
    ComparisonExpr,
    ConditionalExpr,
    DictExpr,
    DictionaryComprehension,
    Expression,
    GeneratorExpr,
    IndexExpr,
    LambdaExpr,
    ListComprehension,
    ListExpr,
    MemberExpr,
    Node,
    OpExpr,
    RevealExpr,
    SetComprehension,
    SetExpr,
    SliceExpr,
    StarExpr,
    TupleExpr,
    TypeApplication,
    UnaryExpr,
    YieldExpr,
    YieldFromExpr,
)
from mypy.traverser import TraverserVisitor


def get_subexpressions(node: Node) -> list[Expression]:
    visitor = SubexpressionFinder()
    node.accept(visitor)
    return visitor.expressions


class SubexpressionFinder(TraverserVisitor):
    def __init__(self) -> None:
        self.expressions: list[Expression] = []

    def visit_int_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_name_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_float_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_str_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_bytes_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_unicode_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_complex_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_ellipsis(self, o: Expression) -> None:
        self.add(o)

    def visit_super_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_type_var_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_type_alias_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_namedtuple_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_typeddict_expr(self, o: Expression) -> None:
        self.add(o)

    def visit__promote_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_newtype_expr(self, o: Expression) -> None:
        self.add(o)

    def visit_member_expr(self, e: MemberExpr) -> None:
        self.add(e)
        super().visit_member_expr(e)

    def visit_yield_from_expr(self, e: YieldFromExpr) -> None:
        self.add(e)
        super().visit_yield_from_expr(e)

    def visit_yield_expr(self, e: YieldExpr) -> None:
        self.add(e)
        super().visit_yield_expr(e)

    def visit_call_expr(self, e: CallExpr) -> None:
        self.add(e)
        super().visit_call_expr(e)

    def visit_op_expr(self, e: OpExpr) -> None:
        self.add(e)
        super().visit_op_expr(e)

    def visit_comparison_expr(self, e: ComparisonExpr) -> None:
        self.add(e)
        super().visit_comparison_expr(e)

    def visit_slice_expr(self, e: SliceExpr) -> None:
        self.add(e)
        super().visit_slice_expr(e)

    def visit_cast_expr(self, e: CastExpr) -> None:
        self.add(e)
        super().visit_cast_expr(e)

    def visit_assert_type_expr(self, e: AssertTypeExpr) -> None:
        self.add(e)
        super().visit_assert_type_expr(e)

    def visit_reveal_expr(self, e: RevealExpr) -> None:
        self.add(e)
        super().visit_reveal_expr(e)

    def visit_assignment_expr(self, e: AssignmentExpr) -> None:
        self.add(e)
        super().visit_assignment_expr(e)

    def visit_unary_expr(self, e: UnaryExpr) -> None:
        self.add(e)
        super().visit_unary_expr(e)

    def visit_list_expr(self, e: ListExpr) -> None:
        self.add(e)
        super().visit_list_expr(e)

    def visit_tuple_expr(self, e: TupleExpr) -> None:
        self.add(e)
        super().visit_tuple_expr(e)

    def visit_dict_expr(self, e: DictExpr) -> None:
        self.add(e)
        super().visit_dict_expr(e)

    def visit_set_expr(self, e: SetExpr) -> None:
        self.add(e)
        super().visit_set_expr(e)

    def visit_index_expr(self, e: IndexExpr) -> None:
        self.add(e)
        super().visit_index_expr(e)

    def visit_generator_expr(self, e: GeneratorExpr) -> None:
        self.add(e)
        super().visit_generator_expr(e)

    def visit_dictionary_comprehension(self, e: DictionaryComprehension) -> None:
        self.add(e)
        super().visit_dictionary_comprehension(e)

    def visit_list_comprehension(self, e: ListComprehension) -> None:
        self.add(e)
        super().visit_list_comprehension(e)

    def visit_set_comprehension(self, e: SetComprehension) -> None:
        self.add(e)
        super().visit_set_comprehension(e)

    def visit_conditional_expr(self, e: ConditionalExpr) -> None:
        self.add(e)
        super().visit_conditional_expr(e)

    def visit_type_application(self, e: TypeApplication) -> None:
        self.add(e)
        super().visit_type_application(e)

    def visit_lambda_expr(self, e: LambdaExpr) -> None:
        self.add(e)
        super().visit_lambda_expr(e)

    def visit_star_expr(self, e: StarExpr) -> None:
        self.add(e)
        super().visit_star_expr(e)

    def visit_await_expr(self, e: AwaitExpr) -> None:
        self.add(e)
        super().visit_await_expr(e)

    def add(self, e: Expression) -> None:
        self.expressions.append(e)
