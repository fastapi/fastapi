"""Unit tests for fastapi.utils helper functions.

These tests cover:
- deep_dict_update
- get_value_or_default (and DefaultPlaceholder semantics)

They are intentionally small and focused to improve coverage and confidence
without changing runtime behavior.
"""

from fastapi import utils
from fastapi.datastructures import Default, DefaultPlaceholder


def test_deep_dict_update_nested_dicts():
    main = {"a": {"b": 1, "c": 2}, "x": 10}
    update = {"a": {"b": 42, "d": 3}}
    utils.deep_dict_update(main, update)
    assert main["a"]["b"] == 42
    assert main["a"]["c"] == 2
    assert main["a"]["d"] == 3
    assert main["x"] == 10


def test_deep_dict_update_lists_concat():
    main = {"lst": [1, 2], "other": "v"}
    update = {"lst": [3, 4]}
    utils.deep_dict_update(main, update)
    assert main["lst"] == [1, 2, 3, 4]
    assert main["other"] == "v"


def test_deep_dict_update_overwrite_on_type_mismatch():
    main = {"k": {"sub": 1}}
    update = {"k": [1, 2, 3]}
    utils.deep_dict_update(main, update)
    assert isinstance(main["k"], list)
    assert main["k"] == [1, 2, 3]


def test_get_value_or_default_returns_first_non_placeholder():
    first = DefaultPlaceholder("first")
    second = Default("real")
    third = DefaultPlaceholder("third")
    result = utils.get_value_or_default(first, second, third)
    assert result == "real"


def test_get_value_or_default_all_placeholders_returns_first():
    first = DefaultPlaceholder("first")
    second = DefaultPlaceholder("second")
    result = utils.get_value_or_default(first, second)
    assert isinstance(result, DefaultPlaceholder)
    assert result.value == "first"


def test_get_value_or_default_handles_falsy_values():
    # Ensure falsy but valid values are returned (e.g., None, False, 0, empty string)
    items = (
        DefaultPlaceholder("x"),
        DefaultPlaceholder("y"),
        0,
        False,
        "",
        None,
    )
    result = utils.get_value_or_default(*items)
    assert result == 0


def test_default_placeholder_bool_and_eq():
    dp_true = Default(1)
    dp_false = Default(0)
    # truthiness uses the inner value
    assert bool(dp_true)
    assert not bool(dp_false)
    # equality compares value
    assert dp_true == DefaultPlaceholder(1)
    assert not (dp_true == dp_false)
