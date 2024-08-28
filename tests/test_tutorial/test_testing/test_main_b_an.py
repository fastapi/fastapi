from docs_src.app_testing.app_b_an import test_main


def test_app():
    test_main.test_create_existing_item()
    test_main.test_create_item()
    test_main.test_create_item_bad_token()
    test_main.test_read_nonexistent_item()
    test_main.test_read_item()
    test_main.test_read_item_bad_token()
