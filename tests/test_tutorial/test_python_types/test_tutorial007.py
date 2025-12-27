from docs_src.python_types.tutorial007_py39 import process_items


def test_process_items():
    items_t = (1, 2, "foo")
    items_s = {b"a", b"b", b"c"}

    assert process_items(items_t, items_s) == (items_t, items_s)
