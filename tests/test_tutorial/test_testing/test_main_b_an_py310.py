from ...utils import needs_py310


@needs_py310
def test_app():
    from docs_src.app_testing.app_b_an_py310 import test_main

    test_main.test_create_existing_item()
    test_main.test_create_item()
    test_main.test_create_item_bad_token()
    test_main.test_read_nonexistent_item()
    test_main.test_read_item()
    test_main.test_read_item_bad_token()
