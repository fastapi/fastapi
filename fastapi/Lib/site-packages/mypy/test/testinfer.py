"""Test cases for type inference helper functions."""

from __future__ import annotations

from mypy.argmap import map_actuals_to_formals
from mypy.checker import DisjointDict, group_comparison_operands
from mypy.literals import Key
from mypy.nodes import (
    ARG_NAMED,
    ARG_OPT,
    ARG_POS,
    ARG_STAR,
    ARG_STAR2,
    ArgKind,
    NameExpr,
)
from mypy.test.helpers import Suite, assert_equal
from mypy.test.typefixture import TypeFixture
from mypy.types import AnyType, TupleType, Type, TypeOfAny


class MapActualsToFormalsSuite(Suite):
    """Test cases for argmap.map_actuals_to_formals."""

    def test_basic(self) -> None:
        self.assert_map([], [], [])

    def test_positional_only(self) -> None:
        self.assert_map([ARG_POS], [ARG_POS], [[0]])
        self.assert_map([ARG_POS, ARG_POS], [ARG_POS, ARG_POS], [[0], [1]])

    def test_optional(self) -> None:
        self.assert_map([], [ARG_OPT], [[]])
        self.assert_map([ARG_POS], [ARG_OPT], [[0]])
        self.assert_map([ARG_POS], [ARG_OPT, ARG_OPT], [[0], []])

    def test_callee_star(self) -> None:
        self.assert_map([], [ARG_STAR], [[]])
        self.assert_map([ARG_POS], [ARG_STAR], [[0]])
        self.assert_map([ARG_POS, ARG_POS], [ARG_STAR], [[0, 1]])

    def test_caller_star(self) -> None:
        self.assert_map([ARG_STAR], [ARG_STAR], [[0]])
        self.assert_map([ARG_POS, ARG_STAR], [ARG_STAR], [[0, 1]])
        self.assert_map([ARG_STAR], [ARG_POS, ARG_STAR], [[0], [0]])
        self.assert_map([ARG_STAR], [ARG_OPT, ARG_STAR], [[0], [0]])

    def test_too_many_caller_args(self) -> None:
        self.assert_map([ARG_POS], [], [])
        self.assert_map([ARG_STAR], [], [])
        self.assert_map([ARG_STAR], [ARG_POS], [[0]])

    def test_tuple_star(self) -> None:
        any_type = AnyType(TypeOfAny.special_form)
        self.assert_vararg_map([ARG_STAR], [ARG_POS], [[0]], self.make_tuple(any_type))
        self.assert_vararg_map(
            [ARG_STAR],
            [ARG_POS, ARG_POS],
            [[0], [0]],
            self.make_tuple(any_type, any_type),
        )
        self.assert_vararg_map(
            [ARG_STAR],
            [ARG_POS, ARG_OPT, ARG_OPT],
            [[0], [0], []],
            self.make_tuple(any_type, any_type),
        )

    def make_tuple(self, *args: Type) -> TupleType:
        return TupleType(list(args), TypeFixture().std_tuple)

    def test_named_args(self) -> None:
        self.assert_map(["x"], [(ARG_POS, "x")], [[0]])
        self.assert_map(["y", "x"], [(ARG_POS, "x"), (ARG_POS, "y")], [[1], [0]])

    def test_some_named_args(self) -> None:
        self.assert_map(
            ["y"], [(ARG_OPT, "x"), (ARG_OPT, "y"), (ARG_OPT, "z")], [[], [0], []]
        )

    def test_missing_named_arg(self) -> None:
        self.assert_map(["y"], [(ARG_OPT, "x")], [[]])

    def test_duplicate_named_arg(self) -> None:
        self.assert_map(["x", "x"], [(ARG_OPT, "x")], [[0, 1]])

    def test_varargs_and_bare_asterisk(self) -> None:
        self.assert_map([ARG_STAR], [ARG_STAR, (ARG_NAMED, "x")], [[0], []])
        self.assert_map([ARG_STAR, "x"], [ARG_STAR, (ARG_NAMED, "x")], [[0], [1]])

    def test_keyword_varargs(self) -> None:
        self.assert_map(["x"], [ARG_STAR2], [[0]])
        self.assert_map(["x", ARG_STAR2], [ARG_STAR2], [[0, 1]])
        self.assert_map(["x", ARG_STAR2], [(ARG_POS, "x"), ARG_STAR2], [[0], [1]])
        self.assert_map([ARG_POS, ARG_STAR2], [(ARG_POS, "x"), ARG_STAR2], [[0], [1]])

    def test_both_kinds_of_varargs(self) -> None:
        self.assert_map(
            [ARG_STAR, ARG_STAR2], [(ARG_POS, "x"), (ARG_POS, "y")], [[0, 1], [0, 1]]
        )

    def test_special_cases(self) -> None:
        self.assert_map([ARG_STAR], [ARG_STAR, ARG_STAR2], [[0], []])
        self.assert_map([ARG_STAR, ARG_STAR2], [ARG_STAR, ARG_STAR2], [[0], [1]])
        self.assert_map([ARG_STAR2], [(ARG_POS, "x"), ARG_STAR2], [[0], [0]])
        self.assert_map([ARG_STAR2], [ARG_STAR2], [[0]])

    def assert_map(
        self,
        caller_kinds_: list[ArgKind | str],
        callee_kinds_: list[ArgKind | tuple[ArgKind, str]],
        expected: list[list[int]],
    ) -> None:
        caller_kinds, caller_names = expand_caller_kinds(caller_kinds_)
        callee_kinds, callee_names = expand_callee_kinds(callee_kinds_)
        result = map_actuals_to_formals(
            caller_kinds,
            caller_names,
            callee_kinds,
            callee_names,
            lambda i: AnyType(TypeOfAny.special_form),
        )
        assert_equal(result, expected)

    def assert_vararg_map(
        self,
        caller_kinds: list[ArgKind],
        callee_kinds: list[ArgKind],
        expected: list[list[int]],
        vararg_type: Type,
    ) -> None:
        result = map_actuals_to_formals(
            caller_kinds, [], callee_kinds, [], lambda i: vararg_type
        )
        assert_equal(result, expected)


def expand_caller_kinds(
    kinds_or_names: list[ArgKind | str],
) -> tuple[list[ArgKind], list[str | None]]:
    kinds = []
    names: list[str | None] = []
    for k in kinds_or_names:
        if isinstance(k, str):
            kinds.append(ARG_NAMED)
            names.append(k)
        else:
            kinds.append(k)
            names.append(None)
    return kinds, names


def expand_callee_kinds(
    kinds_and_names: list[ArgKind | tuple[ArgKind, str]]
) -> tuple[list[ArgKind], list[str | None]]:
    kinds = []
    names: list[str | None] = []
    for v in kinds_and_names:
        if isinstance(v, tuple):
            kinds.append(v[0])
            names.append(v[1])
        else:
            kinds.append(v)
            names.append(None)
    return kinds, names


class OperandDisjointDictSuite(Suite):
    """Test cases for checker.DisjointDict, which is used for type inference with operands."""

    def new(self) -> DisjointDict[int, str]:
        return DisjointDict()

    def test_independent_maps(self) -> None:
        d = self.new()
        d.add_mapping({0, 1}, {"group1"})
        d.add_mapping({2, 3, 4}, {"group2"})
        d.add_mapping({5, 6, 7}, {"group3"})

        self.assertEqual(
            d.items(),
            [({0, 1}, {"group1"}), ({2, 3, 4}, {"group2"}), ({5, 6, 7}, {"group3"})],
        )

    def test_partial_merging(self) -> None:
        d = self.new()
        d.add_mapping({0, 1}, {"group1"})
        d.add_mapping({1, 2}, {"group2"})
        d.add_mapping({3, 4}, {"group3"})
        d.add_mapping({5, 0}, {"group4"})
        d.add_mapping({5, 6}, {"group5"})
        d.add_mapping({4, 7}, {"group6"})

        self.assertEqual(
            d.items(),
            [
                ({0, 1, 2, 5, 6}, {"group1", "group2", "group4", "group5"}),
                ({3, 4, 7}, {"group3", "group6"}),
            ],
        )

    def test_full_merging(self) -> None:
        d = self.new()
        d.add_mapping({0, 1, 2}, {"a"})
        d.add_mapping({3, 4, 2}, {"b"})
        d.add_mapping({10, 11, 12}, {"c"})
        d.add_mapping({13, 14, 15}, {"d"})
        d.add_mapping({14, 10, 16}, {"e"})
        d.add_mapping({0, 10}, {"f"})

        self.assertEqual(
            d.items(),
            [
                (
                    {0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16},
                    {"a", "b", "c", "d", "e", "f"},
                )
            ],
        )

    def test_merge_with_multiple_overlaps(self) -> None:
        d = self.new()
        d.add_mapping({0, 1, 2}, {"a"})
        d.add_mapping({3, 4, 5}, {"b"})
        d.add_mapping({1, 2, 4, 5}, {"c"})
        d.add_mapping({6, 1, 2, 4, 5}, {"d"})
        d.add_mapping({6, 1, 2, 4, 5}, {"e"})

        self.assertEqual(
            d.items(), [({0, 1, 2, 3, 4, 5, 6}, {"a", "b", "c", "d", "e"})]
        )


class OperandComparisonGroupingSuite(Suite):
    """Test cases for checker.group_comparison_operands."""

    def literal_keymap(
        self, assignable_operands: dict[int, NameExpr]
    ) -> dict[int, Key]:
        output: dict[int, Key] = {}
        for index, expr in assignable_operands.items():
            output[index] = ("FakeExpr", expr.name)
        return output

    def test_basic_cases(self) -> None:
        # Note: the grouping function doesn't actually inspect the input exprs, so we
        # just default to using NameExprs for simplicity.
        x0 = NameExpr("x0")
        x1 = NameExpr("x1")
        x2 = NameExpr("x2")
        x3 = NameExpr("x3")
        x4 = NameExpr("x4")

        basic_input = [("==", x0, x1), ("==", x1, x2), ("<", x2, x3), ("==", x3, x4)]

        none_assignable = self.literal_keymap({})
        all_assignable = self.literal_keymap({0: x0, 1: x1, 2: x2, 3: x3, 4: x4})

        for assignable in [none_assignable, all_assignable]:
            self.assertEqual(
                group_comparison_operands(basic_input, assignable, set()),
                [("==", [0, 1]), ("==", [1, 2]), ("<", [2, 3]), ("==", [3, 4])],
            )
            self.assertEqual(
                group_comparison_operands(basic_input, assignable, {"=="}),
                [("==", [0, 1, 2]), ("<", [2, 3]), ("==", [3, 4])],
            )
            self.assertEqual(
                group_comparison_operands(basic_input, assignable, {"<"}),
                [("==", [0, 1]), ("==", [1, 2]), ("<", [2, 3]), ("==", [3, 4])],
            )
            self.assertEqual(
                group_comparison_operands(basic_input, assignable, {"==", "<"}),
                [("==", [0, 1, 2]), ("<", [2, 3]), ("==", [3, 4])],
            )

    def test_multiple_groups(self) -> None:
        x0 = NameExpr("x0")
        x1 = NameExpr("x1")
        x2 = NameExpr("x2")
        x3 = NameExpr("x3")
        x4 = NameExpr("x4")
        x5 = NameExpr("x5")

        self.assertEqual(
            group_comparison_operands(
                [("==", x0, x1), ("==", x1, x2), ("is", x2, x3), ("is", x3, x4)],
                self.literal_keymap({}),
                {"==", "is"},
            ),
            [("==", [0, 1, 2]), ("is", [2, 3, 4])],
        )
        self.assertEqual(
            group_comparison_operands(
                [("==", x0, x1), ("==", x1, x2), ("==", x2, x3), ("==", x3, x4)],
                self.literal_keymap({}),
                {"==", "is"},
            ),
            [("==", [0, 1, 2, 3, 4])],
        )
        self.assertEqual(
            group_comparison_operands(
                [("is", x0, x1), ("==", x1, x2), ("==", x2, x3), ("==", x3, x4)],
                self.literal_keymap({}),
                {"==", "is"},
            ),
            [("is", [0, 1]), ("==", [1, 2, 3, 4])],
        )
        self.assertEqual(
            group_comparison_operands(
                [
                    ("is", x0, x1),
                    ("is", x1, x2),
                    ("<", x2, x3),
                    ("==", x3, x4),
                    ("==", x4, x5),
                ],
                self.literal_keymap({}),
                {"==", "is"},
            ),
            [("is", [0, 1, 2]), ("<", [2, 3]), ("==", [3, 4, 5])],
        )

    def test_multiple_groups_coalescing(self) -> None:
        x0 = NameExpr("x0")
        x1 = NameExpr("x1")
        x2 = NameExpr("x2")
        x3 = NameExpr("x3")
        x4 = NameExpr("x4")

        nothing_combined = [("==", [0, 1, 2]), ("<", [2, 3]), ("==", [3, 4, 5])]
        everything_combined = [("==", [0, 1, 2, 3, 4, 5]), ("<", [2, 3])]

        # Note: We do 'x4 == x0' at the very end!
        two_groups = [
            ("==", x0, x1),
            ("==", x1, x2),
            ("<", x2, x3),
            ("==", x3, x4),
            ("==", x4, x0),
        ]
        self.assertEqual(
            group_comparison_operands(
                two_groups,
                self.literal_keymap({0: x0, 1: x1, 2: x2, 3: x3, 4: x4, 5: x0}),
                {"=="},
            ),
            everything_combined,
            "All vars are assignable, everything is combined",
        )
        self.assertEqual(
            group_comparison_operands(
                two_groups, self.literal_keymap({1: x1, 2: x2, 3: x3, 4: x4}), {"=="}
            ),
            nothing_combined,
            "x0 is unassignable, so no combining",
        )
        self.assertEqual(
            group_comparison_operands(
                two_groups, self.literal_keymap({0: x0, 1: x1, 3: x3, 5: x0}), {"=="}
            ),
            everything_combined,
            "Some vars are unassignable but x0 is, so we combine",
        )
        self.assertEqual(
            group_comparison_operands(
                two_groups, self.literal_keymap({0: x0, 5: x0}), {"=="}
            ),
            everything_combined,
            "All vars are unassignable but x0 is, so we combine",
        )

    def test_multiple_groups_different_operators(self) -> None:
        x0 = NameExpr("x0")
        x1 = NameExpr("x1")
        x2 = NameExpr("x2")
        x3 = NameExpr("x3")

        groups = [("==", x0, x1), ("==", x1, x2), ("is", x2, x3), ("is", x3, x0)]
        keymap = self.literal_keymap({0: x0, 1: x1, 2: x2, 3: x3, 4: x0})
        self.assertEqual(
            group_comparison_operands(groups, keymap, {"==", "is"}),
            [("==", [0, 1, 2]), ("is", [2, 3, 4])],
            "Different operators can never be combined",
        )

    def test_single_pair(self) -> None:
        x0 = NameExpr("x0")
        x1 = NameExpr("x1")

        single_comparison = [("==", x0, x1)]
        expected_output = [("==", [0, 1])]

        assignable_combinations: list[dict[int, NameExpr]] = [
            {},
            {0: x0},
            {1: x1},
            {0: x0, 1: x1},
        ]
        to_group_by: list[set[str]] = [set(), {"=="}, {"is"}]

        for combo in assignable_combinations:
            for operators in to_group_by:
                keymap = self.literal_keymap(combo)
                self.assertEqual(
                    group_comparison_operands(single_comparison, keymap, operators),
                    expected_output,
                )

    def test_empty_pair_list(self) -> None:
        # This case should never occur in practice -- ComparisionExprs
        # always contain at least one comparison. But in case it does...

        self.assertEqual(group_comparison_operands([], {}, set()), [])
        self.assertEqual(group_comparison_operands([], {}, {"=="}), [])
