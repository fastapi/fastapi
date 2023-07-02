"""Base visitor that implements an identity AST transform.

Subclass TransformVisitor to perform non-trivial transformations.
"""

from __future__ import annotations

from typing import Iterable, Optional, cast

from mypy.nodes import (
    GDEF,
    REVEAL_TYPE,
    Argument,
    AssertStmt,
    AssertTypeExpr,
    AssignmentExpr,
    AssignmentStmt,
    AwaitExpr,
    Block,
    BreakStmt,
    BytesExpr,
    CallExpr,
    CastExpr,
    ClassDef,
    ComparisonExpr,
    ComplexExpr,
    ConditionalExpr,
    ContinueStmt,
    Decorator,
    DelStmt,
    DictExpr,
    DictionaryComprehension,
    EllipsisExpr,
    EnumCallExpr,
    Expression,
    ExpressionStmt,
    FloatExpr,
    ForStmt,
    FuncDef,
    FuncItem,
    GeneratorExpr,
    GlobalDecl,
    IfStmt,
    Import,
    ImportAll,
    ImportFrom,
    IndexExpr,
    IntExpr,
    LambdaExpr,
    ListComprehension,
    ListExpr,
    MatchStmt,
    MemberExpr,
    MypyFile,
    NamedTupleExpr,
    NameExpr,
    NewTypeExpr,
    Node,
    NonlocalDecl,
    OperatorAssignmentStmt,
    OpExpr,
    OverloadedFuncDef,
    OverloadPart,
    ParamSpecExpr,
    PassStmt,
    PromoteExpr,
    RaiseStmt,
    RefExpr,
    ReturnStmt,
    RevealExpr,
    SetComprehension,
    SetExpr,
    SliceExpr,
    StarExpr,
    Statement,
    StrExpr,
    SuperExpr,
    SymbolTable,
    TempNode,
    TryStmt,
    TupleExpr,
    TypeAliasExpr,
    TypeApplication,
    TypedDictExpr,
    TypeVarExpr,
    TypeVarTupleExpr,
    UnaryExpr,
    Var,
    WhileStmt,
    WithStmt,
    YieldExpr,
    YieldFromExpr,
)
from mypy.patterns import (
    AsPattern,
    ClassPattern,
    MappingPattern,
    OrPattern,
    Pattern,
    SequencePattern,
    SingletonPattern,
    StarredPattern,
    ValuePattern,
)
from mypy.traverser import TraverserVisitor
from mypy.types import FunctionLike, ProperType, Type
from mypy.util import replace_object_state
from mypy.visitor import NodeVisitor


class TransformVisitor(NodeVisitor[Node]):
    """Transform a semantically analyzed AST (or subtree) to an identical copy.

    Use the node() method to transform an AST node.

    Subclass to perform a non-identity transform.

    Notes:

     * This can only be used to transform functions or classes, not top-level
       statements, and/or modules as a whole.
     * Do not duplicate TypeInfo nodes. This would generally not be desirable.
     * Only update some name binding cross-references, but only those that
       refer to Var, Decorator or FuncDef nodes, not those targeting ClassDef or
       TypeInfo nodes.
     * Types are not transformed, but you can override type() to also perform
       type transformation.

    TODO nested classes and functions have not been tested well enough
    """

    def __init__(self) -> None:
        # To simplify testing, set this flag to True if you want to transform
        # all statements in a file (this is prohibited in normal mode).
        self.test_only = False
        # There may be multiple references to a Var node. Keep track of
        # Var translations using a dictionary.
        self.var_map: dict[Var, Var] = {}
        # These are uninitialized placeholder nodes used temporarily for nested
        # functions while we are transforming a top-level function. This maps an
        # untransformed node to a placeholder (which will later become the
        # transformed node).
        self.func_placeholder_map: dict[FuncDef, FuncDef] = {}

    def visit_mypy_file(self, node: MypyFile) -> MypyFile:
        assert self.test_only, "This visitor should not be used for whole files."
        # NOTE: The 'names' and 'imports' instance variables will be empty!
        ignored_lines = {
            line: codes.copy() for line, codes in node.ignored_lines.items()
        }
        new = MypyFile(
            self.statements(node.defs), [], node.is_bom, ignored_lines=ignored_lines
        )
        new._fullname = node._fullname
        new.path = node.path
        new.names = SymbolTable()
        return new

    def visit_import(self, node: Import) -> Import:
        return Import(node.ids.copy())

    def visit_import_from(self, node: ImportFrom) -> ImportFrom:
        return ImportFrom(node.id, node.relative, node.names.copy())

    def visit_import_all(self, node: ImportAll) -> ImportAll:
        return ImportAll(node.id, node.relative)

    def copy_argument(self, argument: Argument) -> Argument:
        arg = Argument(
            self.visit_var(argument.variable),
            argument.type_annotation,
            argument.initializer,
            argument.kind,
        )

        # Refresh lines of the inner things
        arg.set_line(argument)

        return arg

    def visit_func_def(self, node: FuncDef) -> FuncDef:
        # Note that a FuncDef must be transformed to a FuncDef.

        # These contortions are needed to handle the case of recursive
        # references inside the function being transformed.
        # Set up placeholder nodes for references within this function
        # to other functions defined inside it.
        # Don't create an entry for this function itself though,
        # since we want self-references to point to the original
        # function if this is the top-level node we are transforming.
        init = FuncMapInitializer(self)
        for stmt in node.body.body:
            stmt.accept(init)

        new = FuncDef(
            node.name,
            [self.copy_argument(arg) for arg in node.arguments],
            self.block(node.body),
            cast(Optional[FunctionLike], self.optional_type(node.type)),
        )

        self.copy_function_attributes(new, node)

        new._fullname = node._fullname
        new.is_decorated = node.is_decorated
        new.is_conditional = node.is_conditional
        new.abstract_status = node.abstract_status
        new.is_static = node.is_static
        new.is_class = node.is_class
        new.is_property = node.is_property
        new.is_final = node.is_final
        new.original_def = node.original_def

        if node in self.func_placeholder_map:
            # There is a placeholder definition for this function. Replace
            # the attributes of the placeholder with those form the transformed
            # function. We know that the classes will be identical (otherwise
            # this wouldn't work).
            result = self.func_placeholder_map[node]
            replace_object_state(result, new)
            return result
        else:
            return new

    def visit_lambda_expr(self, node: LambdaExpr) -> LambdaExpr:
        new = LambdaExpr(
            [self.copy_argument(arg) for arg in node.arguments],
            self.block(node.body),
            cast(Optional[FunctionLike], self.optional_type(node.type)),
        )
        self.copy_function_attributes(new, node)
        return new

    def copy_function_attributes(self, new: FuncItem, original: FuncItem) -> None:
        new.info = original.info
        new.min_args = original.min_args
        new.max_pos = original.max_pos
        new.is_overload = original.is_overload
        new.is_generator = original.is_generator
        new.is_coroutine = original.is_coroutine
        new.is_async_generator = original.is_async_generator
        new.is_awaitable_coroutine = original.is_awaitable_coroutine
        new.line = original.line

    def visit_overloaded_func_def(self, node: OverloadedFuncDef) -> OverloadedFuncDef:
        items = [cast(OverloadPart, item.accept(self)) for item in node.items]
        for newitem, olditem in zip(items, node.items):
            newitem.line = olditem.line
        new = OverloadedFuncDef(items)
        new._fullname = node._fullname
        new_type = self.optional_type(node.type)
        assert isinstance(new_type, ProperType)
        new.type = new_type
        new.info = node.info
        new.is_static = node.is_static
        new.is_class = node.is_class
        new.is_property = node.is_property
        new.is_final = node.is_final
        if node.impl:
            new.impl = cast(OverloadPart, node.impl.accept(self))
        return new

    def visit_class_def(self, node: ClassDef) -> ClassDef:
        new = ClassDef(
            node.name,
            self.block(node.defs),
            node.type_vars,
            self.expressions(node.base_type_exprs),
            self.optional_expr(node.metaclass),
        )
        new.fullname = node.fullname
        new.info = node.info
        new.decorators = [self.expr(decorator) for decorator in node.decorators]
        return new

    def visit_global_decl(self, node: GlobalDecl) -> GlobalDecl:
        return GlobalDecl(node.names.copy())

    def visit_nonlocal_decl(self, node: NonlocalDecl) -> NonlocalDecl:
        return NonlocalDecl(node.names.copy())

    def visit_block(self, node: Block) -> Block:
        return Block(self.statements(node.body))

    def visit_decorator(self, node: Decorator) -> Decorator:
        # Note that a Decorator must be transformed to a Decorator.
        func = self.visit_func_def(node.func)
        func.line = node.func.line
        new = Decorator(
            func, self.expressions(node.decorators), self.visit_var(node.var)
        )
        new.is_overload = node.is_overload
        return new

    def visit_var(self, node: Var) -> Var:
        # Note that a Var must be transformed to a Var.
        if node in self.var_map:
            return self.var_map[node]
        new = Var(node.name, self.optional_type(node.type))
        new.line = node.line
        new._fullname = node._fullname
        new.info = node.info
        new.is_self = node.is_self
        new.is_ready = node.is_ready
        new.is_initialized_in_class = node.is_initialized_in_class
        new.is_staticmethod = node.is_staticmethod
        new.is_classmethod = node.is_classmethod
        new.is_property = node.is_property
        new.is_final = node.is_final
        new.final_value = node.final_value
        new.final_unset_in_class = node.final_unset_in_class
        new.final_set_in_init = node.final_set_in_init
        new.set_line(node)
        self.var_map[node] = new
        return new

    def visit_expression_stmt(self, node: ExpressionStmt) -> ExpressionStmt:
        return ExpressionStmt(self.expr(node.expr))

    def visit_assignment_stmt(self, node: AssignmentStmt) -> AssignmentStmt:
        return self.duplicate_assignment(node)

    def duplicate_assignment(self, node: AssignmentStmt) -> AssignmentStmt:
        new = AssignmentStmt(
            self.expressions(node.lvalues),
            self.expr(node.rvalue),
            self.optional_type(node.unanalyzed_type),
        )
        new.line = node.line
        new.is_final_def = node.is_final_def
        new.type = self.optional_type(node.type)
        return new

    def visit_operator_assignment_stmt(
        self, node: OperatorAssignmentStmt
    ) -> OperatorAssignmentStmt:
        return OperatorAssignmentStmt(
            node.op, self.expr(node.lvalue), self.expr(node.rvalue)
        )

    def visit_while_stmt(self, node: WhileStmt) -> WhileStmt:
        return WhileStmt(
            self.expr(node.expr),
            self.block(node.body),
            self.optional_block(node.else_body),
        )

    def visit_for_stmt(self, node: ForStmt) -> ForStmt:
        new = ForStmt(
            self.expr(node.index),
            self.expr(node.expr),
            self.block(node.body),
            self.optional_block(node.else_body),
            self.optional_type(node.unanalyzed_index_type),
        )
        new.is_async = node.is_async
        new.index_type = self.optional_type(node.index_type)
        return new

    def visit_return_stmt(self, node: ReturnStmt) -> ReturnStmt:
        return ReturnStmt(self.optional_expr(node.expr))

    def visit_assert_stmt(self, node: AssertStmt) -> AssertStmt:
        return AssertStmt(self.expr(node.expr), self.optional_expr(node.msg))

    def visit_del_stmt(self, node: DelStmt) -> DelStmt:
        return DelStmt(self.expr(node.expr))

    def visit_if_stmt(self, node: IfStmt) -> IfStmt:
        return IfStmt(
            self.expressions(node.expr),
            self.blocks(node.body),
            self.optional_block(node.else_body),
        )

    def visit_break_stmt(self, node: BreakStmt) -> BreakStmt:
        return BreakStmt()

    def visit_continue_stmt(self, node: ContinueStmt) -> ContinueStmt:
        return ContinueStmt()

    def visit_pass_stmt(self, node: PassStmt) -> PassStmt:
        return PassStmt()

    def visit_raise_stmt(self, node: RaiseStmt) -> RaiseStmt:
        return RaiseStmt(
            self.optional_expr(node.expr), self.optional_expr(node.from_expr)
        )

    def visit_try_stmt(self, node: TryStmt) -> TryStmt:
        new = TryStmt(
            self.block(node.body),
            self.optional_names(node.vars),
            self.optional_expressions(node.types),
            self.blocks(node.handlers),
            self.optional_block(node.else_body),
            self.optional_block(node.finally_body),
        )
        new.is_star = node.is_star
        return new

    def visit_with_stmt(self, node: WithStmt) -> WithStmt:
        new = WithStmt(
            self.expressions(node.expr),
            self.optional_expressions(node.target),
            self.block(node.body),
            self.optional_type(node.unanalyzed_type),
        )
        new.is_async = node.is_async
        new.analyzed_types = [self.type(typ) for typ in node.analyzed_types]
        return new

    def visit_as_pattern(self, p: AsPattern) -> AsPattern:
        return AsPattern(
            pattern=self.pattern(p.pattern) if p.pattern is not None else None,
            name=self.duplicate_name(p.name) if p.name is not None else None,
        )

    def visit_or_pattern(self, p: OrPattern) -> OrPattern:
        return OrPattern([self.pattern(pat) for pat in p.patterns])

    def visit_value_pattern(self, p: ValuePattern) -> ValuePattern:
        return ValuePattern(self.expr(p.expr))

    def visit_singleton_pattern(self, p: SingletonPattern) -> SingletonPattern:
        return SingletonPattern(p.value)

    def visit_sequence_pattern(self, p: SequencePattern) -> SequencePattern:
        return SequencePattern([self.pattern(pat) for pat in p.patterns])

    def visit_starred_pattern(self, p: StarredPattern) -> StarredPattern:
        return StarredPattern(
            self.duplicate_name(p.capture) if p.capture is not None else None
        )

    def visit_mapping_pattern(self, p: MappingPattern) -> MappingPattern:
        return MappingPattern(
            keys=[self.expr(expr) for expr in p.keys],
            values=[self.pattern(pat) for pat in p.values],
            rest=self.duplicate_name(p.rest) if p.rest is not None else None,
        )

    def visit_class_pattern(self, p: ClassPattern) -> ClassPattern:
        class_ref = p.class_ref.accept(self)
        assert isinstance(class_ref, RefExpr)
        return ClassPattern(
            class_ref=class_ref,
            positionals=[self.pattern(pat) for pat in p.positionals],
            keyword_keys=list(p.keyword_keys),
            keyword_values=[self.pattern(pat) for pat in p.keyword_values],
        )

    def visit_match_stmt(self, o: MatchStmt) -> MatchStmt:
        return MatchStmt(
            subject=self.expr(o.subject),
            patterns=[self.pattern(p) for p in o.patterns],
            guards=self.optional_expressions(o.guards),
            bodies=self.blocks(o.bodies),
        )

    def visit_star_expr(self, node: StarExpr) -> StarExpr:
        return StarExpr(node.expr)

    def visit_int_expr(self, node: IntExpr) -> IntExpr:
        return IntExpr(node.value)

    def visit_str_expr(self, node: StrExpr) -> StrExpr:
        return StrExpr(node.value)

    def visit_bytes_expr(self, node: BytesExpr) -> BytesExpr:
        return BytesExpr(node.value)

    def visit_float_expr(self, node: FloatExpr) -> FloatExpr:
        return FloatExpr(node.value)

    def visit_complex_expr(self, node: ComplexExpr) -> ComplexExpr:
        return ComplexExpr(node.value)

    def visit_ellipsis(self, node: EllipsisExpr) -> EllipsisExpr:
        return EllipsisExpr()

    def visit_name_expr(self, node: NameExpr) -> NameExpr:
        return self.duplicate_name(node)

    def duplicate_name(self, node: NameExpr) -> NameExpr:
        # This method is used when the transform result must be a NameExpr.
        # visit_name_expr() is used when there is no such restriction.
        new = NameExpr(node.name)
        self.copy_ref(new, node)
        new.is_special_form = node.is_special_form
        return new

    def visit_member_expr(self, node: MemberExpr) -> MemberExpr:
        member = MemberExpr(self.expr(node.expr), node.name)
        if node.def_var:
            # This refers to an attribute and we don't transform attributes by default,
            # just normal variables.
            member.def_var = node.def_var
        self.copy_ref(member, node)
        return member

    def copy_ref(self, new: RefExpr, original: RefExpr) -> None:
        new.kind = original.kind
        new.fullname = original.fullname
        target = original.node
        if isinstance(target, Var):
            # Do not transform references to global variables. See
            # testGenericFunctionAliasExpand for an example where this is important.
            if original.kind != GDEF:
                target = self.visit_var(target)
        elif isinstance(target, Decorator):
            target = self.visit_var(target.var)
        elif isinstance(target, FuncDef):
            # Use a placeholder node for the function if it exists.
            target = self.func_placeholder_map.get(target, target)
        new.node = target
        new.is_new_def = original.is_new_def
        new.is_inferred_def = original.is_inferred_def

    def visit_yield_from_expr(self, node: YieldFromExpr) -> YieldFromExpr:
        return YieldFromExpr(self.expr(node.expr))

    def visit_yield_expr(self, node: YieldExpr) -> YieldExpr:
        return YieldExpr(self.optional_expr(node.expr))

    def visit_await_expr(self, node: AwaitExpr) -> AwaitExpr:
        return AwaitExpr(self.expr(node.expr))

    def visit_call_expr(self, node: CallExpr) -> CallExpr:
        return CallExpr(
            self.expr(node.callee),
            self.expressions(node.args),
            node.arg_kinds.copy(),
            node.arg_names.copy(),
            self.optional_expr(node.analyzed),
        )

    def visit_op_expr(self, node: OpExpr) -> OpExpr:
        new = OpExpr(
            node.op,
            self.expr(node.left),
            self.expr(node.right),
            cast(Optional[TypeAliasExpr], self.optional_expr(node.analyzed)),
        )
        new.method_type = self.optional_type(node.method_type)
        return new

    def visit_comparison_expr(self, node: ComparisonExpr) -> ComparisonExpr:
        new = ComparisonExpr(node.operators, self.expressions(node.operands))
        new.method_types = [self.optional_type(t) for t in node.method_types]
        return new

    def visit_cast_expr(self, node: CastExpr) -> CastExpr:
        return CastExpr(self.expr(node.expr), self.type(node.type))

    def visit_assert_type_expr(self, node: AssertTypeExpr) -> AssertTypeExpr:
        return AssertTypeExpr(self.expr(node.expr), self.type(node.type))

    def visit_reveal_expr(self, node: RevealExpr) -> RevealExpr:
        if node.kind == REVEAL_TYPE:
            assert node.expr is not None
            return RevealExpr(kind=REVEAL_TYPE, expr=self.expr(node.expr))
        else:
            # Reveal locals expressions don't have any sub expressions
            return node

    def visit_super_expr(self, node: SuperExpr) -> SuperExpr:
        call = self.expr(node.call)
        assert isinstance(call, CallExpr)
        new = SuperExpr(node.name, call)
        new.info = node.info
        return new

    def visit_assignment_expr(self, node: AssignmentExpr) -> AssignmentExpr:
        return AssignmentExpr(self.expr(node.target), self.expr(node.value))

    def visit_unary_expr(self, node: UnaryExpr) -> UnaryExpr:
        new = UnaryExpr(node.op, self.expr(node.expr))
        new.method_type = self.optional_type(node.method_type)
        return new

    def visit_list_expr(self, node: ListExpr) -> ListExpr:
        return ListExpr(self.expressions(node.items))

    def visit_dict_expr(self, node: DictExpr) -> DictExpr:
        return DictExpr(
            [
                (self.expr(key) if key else None, self.expr(value))
                for key, value in node.items
            ]
        )

    def visit_tuple_expr(self, node: TupleExpr) -> TupleExpr:
        return TupleExpr(self.expressions(node.items))

    def visit_set_expr(self, node: SetExpr) -> SetExpr:
        return SetExpr(self.expressions(node.items))

    def visit_index_expr(self, node: IndexExpr) -> IndexExpr:
        new = IndexExpr(self.expr(node.base), self.expr(node.index))
        if node.method_type:
            new.method_type = self.type(node.method_type)
        if node.analyzed:
            if isinstance(node.analyzed, TypeApplication):
                new.analyzed = self.visit_type_application(node.analyzed)
            else:
                new.analyzed = self.visit_type_alias_expr(node.analyzed)
            new.analyzed.set_line(node.analyzed)
        return new

    def visit_type_application(self, node: TypeApplication) -> TypeApplication:
        return TypeApplication(self.expr(node.expr), self.types(node.types))

    def visit_list_comprehension(self, node: ListComprehension) -> ListComprehension:
        generator = self.duplicate_generator(node.generator)
        generator.set_line(node.generator)
        return ListComprehension(generator)

    def visit_set_comprehension(self, node: SetComprehension) -> SetComprehension:
        generator = self.duplicate_generator(node.generator)
        generator.set_line(node.generator)
        return SetComprehension(generator)

    def visit_dictionary_comprehension(
        self, node: DictionaryComprehension
    ) -> DictionaryComprehension:
        return DictionaryComprehension(
            self.expr(node.key),
            self.expr(node.value),
            [self.expr(index) for index in node.indices],
            [self.expr(s) for s in node.sequences],
            [[self.expr(cond) for cond in conditions] for conditions in node.condlists],
            node.is_async,
        )

    def visit_generator_expr(self, node: GeneratorExpr) -> GeneratorExpr:
        return self.duplicate_generator(node)

    def duplicate_generator(self, node: GeneratorExpr) -> GeneratorExpr:
        return GeneratorExpr(
            self.expr(node.left_expr),
            [self.expr(index) for index in node.indices],
            [self.expr(s) for s in node.sequences],
            [[self.expr(cond) for cond in conditions] for conditions in node.condlists],
            node.is_async,
        )

    def visit_slice_expr(self, node: SliceExpr) -> SliceExpr:
        return SliceExpr(
            self.optional_expr(node.begin_index),
            self.optional_expr(node.end_index),
            self.optional_expr(node.stride),
        )

    def visit_conditional_expr(self, node: ConditionalExpr) -> ConditionalExpr:
        return ConditionalExpr(
            self.expr(node.cond), self.expr(node.if_expr), self.expr(node.else_expr)
        )

    def visit_type_var_expr(self, node: TypeVarExpr) -> TypeVarExpr:
        return TypeVarExpr(
            node.name,
            node.fullname,
            self.types(node.values),
            self.type(node.upper_bound),
            self.type(node.default),
            variance=node.variance,
        )

    def visit_paramspec_expr(self, node: ParamSpecExpr) -> ParamSpecExpr:
        return ParamSpecExpr(
            node.name,
            node.fullname,
            self.type(node.upper_bound),
            self.type(node.default),
            variance=node.variance,
        )

    def visit_type_var_tuple_expr(self, node: TypeVarTupleExpr) -> TypeVarTupleExpr:
        return TypeVarTupleExpr(
            node.name,
            node.fullname,
            self.type(node.upper_bound),
            node.tuple_fallback,
            self.type(node.default),
            variance=node.variance,
        )

    def visit_type_alias_expr(self, node: TypeAliasExpr) -> TypeAliasExpr:
        return TypeAliasExpr(node.node)

    def visit_newtype_expr(self, node: NewTypeExpr) -> NewTypeExpr:
        res = NewTypeExpr(node.name, node.old_type, line=node.line, column=node.column)
        res.info = node.info
        return res

    def visit_namedtuple_expr(self, node: NamedTupleExpr) -> NamedTupleExpr:
        return NamedTupleExpr(node.info)

    def visit_enum_call_expr(self, node: EnumCallExpr) -> EnumCallExpr:
        return EnumCallExpr(node.info, node.items, node.values)

    def visit_typeddict_expr(self, node: TypedDictExpr) -> Node:
        return TypedDictExpr(node.info)

    def visit__promote_expr(self, node: PromoteExpr) -> PromoteExpr:
        return PromoteExpr(node.type)

    def visit_temp_node(self, node: TempNode) -> TempNode:
        return TempNode(self.type(node.type))

    def node(self, node: Node) -> Node:
        new = node.accept(self)
        new.set_line(node)
        return new

    def mypyfile(self, node: MypyFile) -> MypyFile:
        new = node.accept(self)
        assert isinstance(new, MypyFile)
        new.set_line(node)
        return new

    def expr(self, expr: Expression) -> Expression:
        new = expr.accept(self)
        assert isinstance(new, Expression)
        new.set_line(expr)
        return new

    def stmt(self, stmt: Statement) -> Statement:
        new = stmt.accept(self)
        assert isinstance(new, Statement)
        new.set_line(stmt)
        return new

    def pattern(self, pattern: Pattern) -> Pattern:
        new = pattern.accept(self)
        assert isinstance(new, Pattern)
        new.set_line(pattern)
        return new

    # Helpers
    #
    # All the node helpers also propagate line numbers.

    def optional_expr(self, expr: Expression | None) -> Expression | None:
        if expr:
            return self.expr(expr)
        else:
            return None

    def block(self, block: Block) -> Block:
        new = self.visit_block(block)
        new.line = block.line
        return new

    def optional_block(self, block: Block | None) -> Block | None:
        if block:
            return self.block(block)
        else:
            return None

    def statements(self, statements: list[Statement]) -> list[Statement]:
        return [self.stmt(stmt) for stmt in statements]

    def expressions(self, expressions: list[Expression]) -> list[Expression]:
        return [self.expr(expr) for expr in expressions]

    def optional_expressions(
        self, expressions: Iterable[Expression | None]
    ) -> list[Expression | None]:
        return [self.optional_expr(expr) for expr in expressions]

    def blocks(self, blocks: list[Block]) -> list[Block]:
        return [self.block(block) for block in blocks]

    def names(self, names: list[NameExpr]) -> list[NameExpr]:
        return [self.duplicate_name(name) for name in names]

    def optional_names(self, names: Iterable[NameExpr | None]) -> list[NameExpr | None]:
        result: list[NameExpr | None] = []
        for name in names:
            if name:
                result.append(self.duplicate_name(name))
            else:
                result.append(None)
        return result

    def type(self, type: Type) -> Type:
        # Override this method to transform types.
        return type

    def optional_type(self, type: Type | None) -> Type | None:
        if type:
            return self.type(type)
        else:
            return None

    def types(self, types: list[Type]) -> list[Type]:
        return [self.type(type) for type in types]


class FuncMapInitializer(TraverserVisitor):
    """This traverser creates mappings from nested FuncDefs to placeholder FuncDefs.

    The placeholders will later be replaced with transformed nodes.
    """

    def __init__(self, transformer: TransformVisitor) -> None:
        self.transformer = transformer

    def visit_func_def(self, node: FuncDef) -> None:
        if node not in self.transformer.func_placeholder_map:
            # Haven't seen this FuncDef before, so create a placeholder node.
            self.transformer.func_placeholder_map[node] = FuncDef(
                node.name, node.arguments, node.body, None
            )
        super().visit_func_def(node)
