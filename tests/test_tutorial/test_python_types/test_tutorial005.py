from docs_src.python_types.tutorial005_py310 import get_items


def test_get_items():
    res = get_items(
        "item_a",
        "item_b",  # ty: ignore[invalid-argument-type]
        "item_c",  # ty: ignore[invalid-argument-type]
        "item_d",  # ty: ignore[invalid-argument-type]
        "item_e",  # ty: ignore[invalid-argument-type]
    )
    assert res == ("item_a", "item_b", "item_c", "item_d", "item_e")
