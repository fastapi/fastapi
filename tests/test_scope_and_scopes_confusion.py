import pytest
from fastapi import Depends, Security
from fastapi.exceptions import FastAPIError


def test_scopes_deprecation_warning():
    """
    Test that using `scopes` parameter raises a deprecation warning.
    """

    with pytest.warns(DeprecationWarning) as record:
        Security(dependency=lambda: None, scopes=["admin"])

    assert len(record) == 1
    warning = record[0]
    assert issubclass(warning.category, DeprecationWarning)
    assert str(warning.message) == (
        "The 'scopes' parameter in Security() is deprecated in favor of "
        "'oauth_scopes' in order to avoid confusion with 'scope' parameter."
    )


@pytest.mark.parametrize("parameter_name", ["scopes", "oauth_scopes"])
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_pass_single_str(parameter_name: str):
    """
    Test passing single string instead of list of strings to `scopes` or `oauth_scopes`.
    """

    with pytest.raises(FastAPIError) as exc_info:
        Security(dependency=lambda: None, **{parameter_name: "admin"})

    assert str(exc_info.value) == (
        f"Invalid value for the '{parameter_name}' parameter in Security(). "
        "Expected a sequence of strings (e.g., ['admin', 'user']), but received a single string. "
        "Wrap it in a list: oauth_scopes=['your_scope'] instead of oauth_scopes='your_scope'."
    )


@pytest.mark.parametrize("value", ["function", "request"])
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_pass_scope_as_scopes(value: str):
    """
    Test passing `scopes="function"` instead of `scope="function"` to `Security`.
    """

    with pytest.raises(FastAPIError) as exc_info:
        Security(dependency=lambda: None, scopes=value)

    assert str(exc_info.value) == (
        "Invalid value for the 'scopes' parameter in Security(). "
        "Expected a sequence of strings (e.g., ['admin', 'user']), but received a single string. "
        f'Did you mean to use scope="{value}" to specify when the exit code of dependencies with yield should run? '
    )


def test_pass_invalid_scope_value_to_security():
    """
    Test passing invalid value to `scope` parameter in `Security`.
    """

    with pytest.raises(FastAPIError) as exc_info:
        Security(dependency=lambda: None, scope="invalid_scope")

    assert str(exc_info.value) == (
        "Invalid value for 'scope' parameter in Security(). "
        "Expected 'function', 'request', or None. "
        'Did you mean oauth_scopes="invalid_scope" to specify OAuth2 scopes instead?'
    )


def test_pass_invalid_scope_value_to_depends():
    """
    Test passing invalid value to `scope` parameter in `Depends`.
    """

    with pytest.raises(FastAPIError) as exc_info:
        Depends(dependency=lambda: None, scope="invalid_scope")

    assert str(exc_info.value) == (
        "Invalid value for 'scope' parameter in Depends(). "
        "Expected 'function', 'request', or None. "
        'Did you mean to use Security(dependency_fn, oauth_scopes="invalid_scope") to specify OAuth2 scopes instead?'
    )
