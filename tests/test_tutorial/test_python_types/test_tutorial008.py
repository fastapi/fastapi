from unittest.mock import patch

from docs_src.python_types.tutorial008_py39 import process_items


def test_process_items():
    with patch("builtins.print") as mock_print:
        process_items({"a": 1.0, "b": 2.5})

    assert mock_print.call_count == 4
    call_args = [arg.args for arg in mock_print.call_args_list]
    assert call_args == [
        ("a",),
        (1.0,),
        ("b",),
        (2.5,),
    ]
