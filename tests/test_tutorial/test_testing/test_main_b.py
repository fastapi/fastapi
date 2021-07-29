from docs_src.app_testing import test_main_b


def test_app():
    test_main_b.test_create_existing_item()
    test_main_b.test_create_item()
    test_main_b.test_create_item_bad_token()
    test_main_b.test_read_inexistent_item()
    test_main_b.test_read_item()
    test_main_b.test_read_item_bad_token()
