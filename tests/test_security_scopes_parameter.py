import pytest
from fastapi import Security
from fastapi.exceptions import FastAPIError


def test_pass_single_str():
    with pytest.raises(FastAPIError) as exc_info:
        Security(dependency=lambda: None, scopes="admin")

    assert str(exc_info.value) == (
        "Invalid value for `scopes` parameter in Security(). "
        "Expected a sequence of strings (e.g., ['admin', 'user']), but received a single string. "
        "Wrap it in a list: scopes=['your_scope'] instead of scopes='your_scope'."
    )


@pytest.mark.parametrize("value", ["function", "request"])
def test_pass_scope_instead_of_scopes(value: str):
    with pytest.raises(FastAPIError) as exc_info:
        Security(dependency=lambda: None, scopes=value)

    assert str(exc_info.value) == (
        "Invalid value for `scopes` parameter in Security(). "
        "You probably meant to use the `scope` parameter instead of `scopes`. "
        "Expected a sequence of strings (e.g., ['admin', 'user']), but received a single string."
    )
