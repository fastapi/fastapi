from docs_src.python_types.tutorial005_py39 import get_items


def test_get_items():
    res = get_items(
        "item_a",
        "item_b",
        "item_c",
        "item_d",
        "item_e",
    )
    assert res == ("item_a", "item_b", "item_c", "item_d", "item_e")
