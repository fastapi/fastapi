from __future__ import annotations

from enum import Enum

from mypy import checker, errorcodes
from mypy.messages import MessageBuilder
from mypy.nodes import (
    AssertStmt,
    AssignmentExpr,
    AssignmentStmt,
    BreakStmt,
    ClassDef,
    Context,
    ContinueStmt,
    DictionaryComprehension,
    Expression,
    ExpressionStmt,
    ForStmt,
    FuncDef,
    FuncItem,
    GeneratorExpr,
    GlobalDecl,
    IfStmt,
    Import,
    ImportFrom,
    LambdaExpr,
    ListExpr,
    Lvalue,
    MatchStmt,
    MypyFile,
    NameExpr,
    NonlocalDecl,
    RaiseStmt,
    ReturnStmt,
    StarExpr,
    SymbolTable,
    TryStmt,
    TupleExpr,
    WhileStmt,
    WithStmt,
    implicit_module_attrs,
)
from mypy.options import Options
from mypy.patterns import AsPattern, StarredPattern
from mypy.reachability import ALWAYS_TRUE, infer_pattern_value
from mypy.traverser import ExtendedTraverserVisitor
from mypy.types import Type, UninhabitedType


class BranchState:
    """BranchState contains information about variable definition at the end of a branching statement.
    `if` and `match` are examples of branching statements.

    `may_be_defined` contains variables that were defined in only some branches.
    `must_be_defined` contains variables that were defined in all branches.
    """

    def __init__(
        self,
        must_be_defined: set[str] | None = None,
        may_be_defined: set[str] | None = None,
        skipped: bool = False,
    ) -> None:
        if may_be_defined is None:
            may_be_defined = set()
        if must_be_defined is None:
            must_be_defined = set()

        self.may_be_defined = set(may_be_defined)
        self.must_be_defined = set(must_be_defined)
        self.skipped = skipped

    def copy(self) -> BranchState:
        return BranchState(
            must_be_defined=set(self.must_be_defined),
            may_be_defined=set(self.may_be_defined),
            skipped=self.skipped,
        )


class BranchStatement:
    def __init__(self, initial_state: BranchState | None = None) -> None:
        if initial_state is None:
            initial_state = BranchState()
        self.initial_state = initial_state
        self.branches: list[BranchState] = [
            BranchState(
                must_be_defined=self.initial_state.must_be_defined,
                may_be_defined=self.initial_state.may_be_defined,
            )
        ]

    def copy(self) -> BranchStatement:
        result = BranchStatement(self.initial_state)
        result.branches = [b.copy() for b in self.branches]
        return result

    def next_branch(self) -> None:
        self.branches.append(
            BranchState(
                must_be_defined=self.initial_state.must_be_defined,
                may_be_defined=self.initial_state.may_be_defined,
            )
        )

    def record_definition(self, name: str) -> None:
        assert len(self.branches) > 0
        self.branches[-1].must_be_defined.add(name)
        self.branches[-1].may_be_defined.discard(name)

    def delete_var(self, name: str) -> None:
        assert len(self.branches) > 0
        self.branches[-1].must_be_defined.discard(name)
        self.branches[-1].may_be_defined.discard(name)

    def record_nested_branch(self, state: BranchState) -> None:
        assert len(self.branches) > 0
        current_branch = self.branches[-1]
        if state.skipped:
            current_branch.skipped = True
            return
        current_branch.must_be_defined.update(state.must_be_defined)
        current_branch.may_be_defined.update(state.may_be_defined)
        current_branch.may_be_defined.difference_update(current_branch.must_be_defined)

    def skip_branch(self) -> None:
        assert len(self.branches) > 0
        self.branches[-1].skipped = True

    def is_possibly_undefined(self, name: str) -> bool:
        assert len(self.branches) > 0
        return name in self.branches[-1].may_be_defined

    def is_undefined(self, name: str) -> bool:
        assert len(self.branches) > 0
        branch = self.branches[-1]
        return name not in branch.may_be_defined and name not in branch.must_be_defined

    def is_defined_in_a_branch(self, name: str) -> bool:
        assert len(self.branches) > 0
        for b in self.branches:
            if name in b.must_be_defined or name in b.may_be_defined:
                return True
        return False

    def done(self) -> BranchState:
        # First, compute all vars, including skipped branches. We include skipped branches
        # because our goal is to capture all variables that semantic analyzer would
        # consider defined.
        all_vars = set()
        for b in self.branches:
            all_vars.update(b.may_be_defined)
            all_vars.update(b.must_be_defined)
        # For the rest of the things, we only care about branches that weren't skipped.
        non_skipped_branches = [b for b in self.branches if not b.skipped]
        if non_skipped_branches:
            must_be_defined = non_skipped_branches[0].must_be_defined
            for b in non_skipped_branches[1:]:
                must_be_defined.intersection_update(b.must_be_defined)
        else:
            must_be_defined = set()
        # Everything that wasn't defined in all branches but was defined
        # in at least one branch should be in `may_be_defined`!
        may_be_defined = all_vars.difference(must_be_defined)
        return BranchState(
            must_be_defined=must_be_defined,
            may_be_defined=may_be_defined,
            skipped=len(non_skipped_branches) == 0,
        )


class ScopeType(Enum):
    Global = 1
    Class = 2
    Func = 3
    Generator = 4


class Scope:
    def __init__(self, stmts: list[BranchStatement], scope_type: ScopeType) -> None:
        self.branch_stmts: list[BranchStatement] = stmts
        self.scope_type = scope_type
        self.undefined_refs: dict[str, set[NameExpr]] = {}

    def copy(self) -> Scope:
        result = Scope([s.copy() for s in self.branch_stmts], self.scope_type)
        result.undefined_refs = self.undefined_refs.copy()
        return result

    def record_undefined_ref(self, o: NameExpr) -> None:
        if o.name not in self.undefined_refs:
            self.undefined_refs[o.name] = set()
        self.undefined_refs[o.name].add(o)

    def pop_undefined_ref(self, name: str) -> set[NameExpr]:
        return self.undefined_refs.pop(name, set())


class DefinedVariableTracker:
    """DefinedVariableTracker manages the state and scope for the UndefinedVariablesVisitor."""

    def __init__(self) -> None:
        # There's always at least one scope. Within each scope, there's at least one "global" BranchingStatement.
        self.scopes: list[Scope] = [Scope([BranchStatement()], ScopeType.Global)]
        # disable_branch_skip is used to disable skipping a branch due to a return/raise/etc. This is useful
        # in things like try/except/finally statements.
        self.disable_branch_skip = False

    def copy(self) -> DefinedVariableTracker:
        result = DefinedVariableTracker()
        result.scopes = [s.copy() for s in self.scopes]
        result.disable_branch_skip = self.disable_branch_skip
        return result

    def _scope(self) -> Scope:
        assert len(self.scopes) > 0
        return self.scopes[-1]

    def enter_scope(self, scope_type: ScopeType) -> None:
        assert len(self._scope().branch_stmts) > 0
        initial_state = None
        if scope_type == ScopeType.Generator:
            # Generators are special because they inherit the outer scope.
            initial_state = self._scope().branch_stmts[-1].branches[-1]
        self.scopes.append(Scope([BranchStatement(initial_state)], scope_type))

    def exit_scope(self) -> None:
        self.scopes.pop()

    def in_scope(self, scope_type: ScopeType) -> bool:
        return self._scope().scope_type == scope_type

    def start_branch_statement(self) -> None:
        assert len(self._scope().branch_stmts) > 0
        self._scope().branch_stmts.append(
            BranchStatement(self._scope().branch_stmts[-1].branches[-1])
        )

    def next_branch(self) -> None:
        assert len(self._scope().branch_stmts) > 1
        self._scope().branch_stmts[-1].next_branch()

    def end_branch_statement(self) -> None:
        assert len(self._scope().branch_stmts) > 1
        result = self._scope().branch_stmts.pop().done()
        self._scope().branch_stmts[-1].record_nested_branch(result)

    def skip_branch(self) -> None:
        # Only skip branch if we're outside of "root" branch statement.
        if len(self._scope().branch_stmts) > 1 and not self.disable_branch_skip:
            self._scope().branch_stmts[-1].skip_branch()

    def record_definition(self, name: str) -> None:
        assert len(self.scopes) > 0
        assert len(self.scopes[-1].branch_stmts) > 0
        self._scope().branch_stmts[-1].record_definition(name)

    def delete_var(self, name: str) -> None:
        assert len(self.scopes) > 0
        assert len(self.scopes[-1].branch_stmts) > 0
        self._scope().branch_stmts[-1].delete_var(name)

    def record_undefined_ref(self, o: NameExpr) -> None:
        """Records an undefined reference. These can later be retrieved via `pop_undefined_ref`."""
        assert len(self.scopes) > 0
        self._scope().record_undefined_ref(o)

    def pop_undefined_ref(self, name: str) -> set[NameExpr]:
        """If name has previously been reported as undefined, the NameExpr that was called will be returned."""
        assert len(self.scopes) > 0
        return self._scope().pop_undefined_ref(name)

    def is_possibly_undefined(self, name: str) -> bool:
        assert len(self._scope().branch_stmts) > 0
        # A variable is undefined if it's in a set of `may_be_defined` but not in `must_be_defined`.
        return self._scope().branch_stmts[-1].is_possibly_undefined(name)

    def is_defined_in_different_branch(self, name: str) -> bool:
        """This will return true if a variable is defined in a branch that's not the current branch."""
        assert len(self._scope().branch_stmts) > 0
        stmt = self._scope().branch_stmts[-1]
        if not stmt.is_undefined(name):
            return False
        for stmt in self._scope().branch_stmts:
            if stmt.is_defined_in_a_branch(name):
                return True
        return False

    def is_undefined(self, name: str) -> bool:
        assert len(self._scope().branch_stmts) > 0
        return self._scope().branch_stmts[-1].is_undefined(name)


class Loop:
    def __init__(self) -> None:
        self.has_break = False


class PossiblyUndefinedVariableVisitor(ExtendedTraverserVisitor):
    """Detects the following cases:
    - A variable that's defined only part of the time.
    - If a variable is used before definition

    An example of a partial definition:
    if foo():
        x = 1
    print(x)  # Error: "x" may be undefined.

    Example of a used before definition:
    x = y
    y: int = 2

    Note that this code does not detect variables not defined in any of the branches -- that is
    handled by the semantic analyzer.
    """

    def __init__(
        self,
        msg: MessageBuilder,
        type_map: dict[Expression, Type],
        options: Options,
        names: SymbolTable,
    ) -> None:
        self.msg = msg
        self.type_map = type_map
        self.options = options
        self.builtins = SymbolTable()
        builtins_mod = names.get("__builtins__", None)
        if builtins_mod:
            assert isinstance(builtins_mod.node, MypyFile)
            self.builtins = builtins_mod.node.names
        self.loops: list[Loop] = []
        self.try_depth = 0
        self.tracker = DefinedVariableTracker()
        for name in implicit_module_attrs:
            self.tracker.record_definition(name)

    def var_used_before_def(self, name: str, context: Context) -> None:
        if self.msg.errors.is_error_code_enabled(errorcodes.USED_BEFORE_DEF):
            self.msg.var_used_before_def(name, context)

    def variable_may_be_undefined(self, name: str, context: Context) -> None:
        if self.msg.errors.is_error_code_enabled(errorcodes.POSSIBLY_UNDEFINED):
            self.msg.variable_may_be_undefined(name, context)

    def process_definition(self, name: str) -> None:
        # Was this name previously used? If yes, it's a used-before-definition error.
        if not self.tracker.in_scope(ScopeType.Class):
            refs = self.tracker.pop_undefined_ref(name)
            for ref in refs:
                if self.loops:
                    self.variable_may_be_undefined(name, ref)
                else:
                    self.var_used_before_def(name, ref)
        else:
            # Errors in class scopes are caught by the semantic analyzer.
            pass
        self.tracker.record_definition(name)

    def visit_global_decl(self, o: GlobalDecl) -> None:
        for name in o.names:
            self.process_definition(name)
        super().visit_global_decl(o)

    def visit_nonlocal_decl(self, o: NonlocalDecl) -> None:
        for name in o.names:
            self.process_definition(name)
        super().visit_nonlocal_decl(o)

    def process_lvalue(self, lvalue: Lvalue | None) -> None:
        if isinstance(lvalue, NameExpr):
            self.process_definition(lvalue.name)
        elif isinstance(lvalue, StarExpr):
            self.process_lvalue(lvalue.expr)
        elif isinstance(lvalue, (ListExpr, TupleExpr)):
            for item in lvalue.items:
                self.process_lvalue(item)

    def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
        for lvalue in o.lvalues:
            self.process_lvalue(lvalue)
        super().visit_assignment_stmt(o)

    def visit_assignment_expr(self, o: AssignmentExpr) -> None:
        o.value.accept(self)
        self.process_lvalue(o.target)

    def visit_if_stmt(self, o: IfStmt) -> None:
        for e in o.expr:
            e.accept(self)
        self.tracker.start_branch_statement()
        for b in o.body:
            if b.is_unreachable:
                continue
            b.accept(self)
            self.tracker.next_branch()
        if o.else_body:
            if not o.else_body.is_unreachable:
                o.else_body.accept(self)
            else:
                self.tracker.skip_branch()
        self.tracker.end_branch_statement()

    def visit_match_stmt(self, o: MatchStmt) -> None:
        o.subject.accept(self)
        self.tracker.start_branch_statement()
        for i in range(len(o.patterns)):
            pattern = o.patterns[i]
            pattern.accept(self)
            guard = o.guards[i]
            if guard is not None:
                guard.accept(self)
            if not o.bodies[i].is_unreachable:
                o.bodies[i].accept(self)
            else:
                self.tracker.skip_branch()
            is_catchall = infer_pattern_value(pattern) == ALWAYS_TRUE
            if not is_catchall:
                self.tracker.next_branch()
        self.tracker.end_branch_statement()

    def visit_func_def(self, o: FuncDef) -> None:
        self.process_definition(o.name)
        super().visit_func_def(o)

    def visit_func(self, o: FuncItem) -> None:
        if o.is_dynamic() and not self.options.check_untyped_defs:
            return

        args = o.arguments or []
        # Process initializers (defaults) outside the function scope.
        for arg in args:
            if arg.initializer is not None:
                arg.initializer.accept(self)

        self.tracker.enter_scope(ScopeType.Func)
        for arg in args:
            self.process_definition(arg.variable.name)
            super().visit_var(arg.variable)
        o.body.accept(self)
        self.tracker.exit_scope()

    def visit_generator_expr(self, o: GeneratorExpr) -> None:
        self.tracker.enter_scope(ScopeType.Generator)
        for idx in o.indices:
            self.process_lvalue(idx)
        super().visit_generator_expr(o)
        self.tracker.exit_scope()

    def visit_dictionary_comprehension(self, o: DictionaryComprehension) -> None:
        self.tracker.enter_scope(ScopeType.Generator)
        for idx in o.indices:
            self.process_lvalue(idx)
        super().visit_dictionary_comprehension(o)
        self.tracker.exit_scope()

    def visit_for_stmt(self, o: ForStmt) -> None:
        o.expr.accept(self)
        self.process_lvalue(o.index)
        o.index.accept(self)
        self.tracker.start_branch_statement()
        loop = Loop()
        self.loops.append(loop)
        o.body.accept(self)
        self.tracker.next_branch()
        self.tracker.end_branch_statement()
        if o.else_body is not None:
            # If the loop has a `break` inside, `else` is executed conditionally.
            # If the loop doesn't have a `break` either the function will return or
            # execute the `else`.
            has_break = loop.has_break
            if has_break:
                self.tracker.start_branch_statement()
                self.tracker.next_branch()
            o.else_body.accept(self)
            if has_break:
                self.tracker.end_branch_statement()
        self.loops.pop()

    def visit_return_stmt(self, o: ReturnStmt) -> None:
        super().visit_return_stmt(o)
        self.tracker.skip_branch()

    def visit_lambda_expr(self, o: LambdaExpr) -> None:
        self.tracker.enter_scope(ScopeType.Func)
        super().visit_lambda_expr(o)
        self.tracker.exit_scope()

    def visit_assert_stmt(self, o: AssertStmt) -> None:
        super().visit_assert_stmt(o)
        if checker.is_false_literal(o.expr):
            self.tracker.skip_branch()

    def visit_raise_stmt(self, o: RaiseStmt) -> None:
        super().visit_raise_stmt(o)
        self.tracker.skip_branch()

    def visit_continue_stmt(self, o: ContinueStmt) -> None:
        super().visit_continue_stmt(o)
        self.tracker.skip_branch()

    def visit_break_stmt(self, o: BreakStmt) -> None:
        super().visit_break_stmt(o)
        if self.loops:
            self.loops[-1].has_break = True
        self.tracker.skip_branch()

    def visit_expression_stmt(self, o: ExpressionStmt) -> None:
        if isinstance(self.type_map.get(o.expr, None), UninhabitedType):
            self.tracker.skip_branch()
        super().visit_expression_stmt(o)

    def visit_try_stmt(self, o: TryStmt) -> None:
        """
        Note that finding undefined vars in `finally` requires different handling from
        the rest of the code. In particular, we want to disallow skipping branches due to jump
        statements in except/else clauses for finally but not for other cases. Imagine a case like:
        def f() -> int:
            try:
                x = 1
            except:
                # This jump statement needs to be handled differently depending on whether or
                # not we're trying to process `finally` or not.
                return 0
            finally:
                # `x` may be undefined here.
                pass
            # `x` is always defined here.
            return x
        """
        self.try_depth += 1
        if o.finally_body is not None:
            # In order to find undefined vars in `finally`, we need to
            # process try/except with branch skipping disabled. However, for the rest of the code
            # after finally, we need to process try/except with branch skipping enabled.
            # Therefore, we need to process try/finally twice.
            # Because processing is not idempotent, we should make a copy of the tracker.
            old_tracker = self.tracker.copy()
            self.tracker.disable_branch_skip = True
            self.process_try_stmt(o)
            self.tracker = old_tracker
        self.process_try_stmt(o)
        self.try_depth -= 1

    def process_try_stmt(self, o: TryStmt) -> None:
        """
        Processes try statement decomposing it into the following:
        if ...:
            body
            else_body
        elif ...:
            except 1
        elif ...:
            except 2
        else:
            except n
        finally
        """
        self.tracker.start_branch_statement()
        o.body.accept(self)
        if o.else_body is not None:
            o.else_body.accept(self)
        if len(o.handlers) > 0:
            assert len(o.handlers) == len(o.vars) == len(o.types)
            for i in range(len(o.handlers)):
                self.tracker.next_branch()
                exc_type = o.types[i]
                if exc_type is not None:
                    exc_type.accept(self)
                var = o.vars[i]
                if var is not None:
                    self.process_definition(var.name)
                    var.accept(self)
                o.handlers[i].accept(self)
                if var is not None:
                    self.tracker.delete_var(var.name)
        self.tracker.end_branch_statement()

        if o.finally_body is not None:
            o.finally_body.accept(self)

    def visit_while_stmt(self, o: WhileStmt) -> None:
        o.expr.accept(self)
        self.tracker.start_branch_statement()
        loop = Loop()
        self.loops.append(loop)
        o.body.accept(self)
        has_break = loop.has_break
        if not checker.is_true_literal(o.expr):
            # If this is a loop like `while True`, we can consider the body to be
            # a single branch statement (we're guaranteed that the body is executed at least once).
            # If not, call next_branch() to make all variables defined there conditional.
            self.tracker.next_branch()
        self.tracker.end_branch_statement()
        if o.else_body is not None:
            # If the loop has a `break` inside, `else` is executed conditionally.
            # If the loop doesn't have a `break` either the function will return or
            # execute the `else`.
            if has_break:
                self.tracker.start_branch_statement()
                self.tracker.next_branch()
            if o.else_body:
                o.else_body.accept(self)
            if has_break:
                self.tracker.end_branch_statement()
        self.loops.pop()

    def visit_as_pattern(self, o: AsPattern) -> None:
        if o.name is not None:
            self.process_lvalue(o.name)
        super().visit_as_pattern(o)

    def visit_starred_pattern(self, o: StarredPattern) -> None:
        if o.capture is not None:
            self.process_lvalue(o.capture)
        super().visit_starred_pattern(o)

    def visit_name_expr(self, o: NameExpr) -> None:
        if o.name in self.builtins and self.tracker.in_scope(ScopeType.Global):
            return
        if self.tracker.is_possibly_undefined(o.name):
            # A variable is only defined in some branches.
            self.variable_may_be_undefined(o.name, o)
            # We don't want to report the error on the same variable multiple times.
            self.tracker.record_definition(o.name)
        elif self.tracker.is_defined_in_different_branch(o.name):
            # A variable is defined in one branch but used in a different branch.
            if self.loops or self.try_depth > 0:
                # If we're in a loop or in a try, we can't be sure that this variable
                # is undefined. Report it as "may be undefined".
                self.variable_may_be_undefined(o.name, o)
            else:
                self.var_used_before_def(o.name, o)
        elif self.tracker.is_undefined(o.name):
            # A variable is undefined. It could be due to two things:
            # 1. A variable is just totally undefined
            # 2. The variable is defined later in the code.
            # Case (1) will be caught by semantic analyzer. Case (2) is a forward ref that should
            # be caught by this visitor. Save the ref for later, so that if we see a definition,
            # we know it's a used-before-definition scenario.
            self.tracker.record_undefined_ref(o)
        super().visit_name_expr(o)

    def visit_with_stmt(self, o: WithStmt) -> None:
        for expr, idx in zip(o.expr, o.target):
            expr.accept(self)
            self.process_lvalue(idx)
        o.body.accept(self)

    def visit_class_def(self, o: ClassDef) -> None:
        self.process_definition(o.name)
        self.tracker.enter_scope(ScopeType.Class)
        super().visit_class_def(o)
        self.tracker.exit_scope()

    def visit_import(self, o: Import) -> None:
        for mod, alias in o.ids:
            if alias is not None:
                self.tracker.record_definition(alias)
            else:
                # When you do `import x.y`, only `x` becomes defined.
                names = mod.split(".")
                if names:
                    # `names` should always be nonempty, but we don't want mypy
                    # to crash on invalid code.
                    self.tracker.record_definition(names[0])
        super().visit_import(o)

    def visit_import_from(self, o: ImportFrom) -> None:
        for mod, alias in o.names:
            name = alias
            if name is None:
                name = mod
            self.tracker.record_definition(name)
        super().visit_import_from(o)
