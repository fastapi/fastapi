import pytest

from docs_src.python_types.tutorial003_py39 import get_name_with_age


def test_get_name_with_age_pass_int():
    with pytest.raises(TypeError):
        get_name_with_age("John", 30)


def test_get_name_with_age_pass_str():
    assert get_name_with_age("John", "30") == "John is this old: 30"
