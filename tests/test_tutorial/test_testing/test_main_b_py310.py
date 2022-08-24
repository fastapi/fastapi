import sys
from pathlib import Path

from ...utils import needs_py310


@needs_py310
def test_app():
    current_path = sys.path.copy()
    import docs_src.app_testing.app_b_py310

    testing_path = Path(docs_src.app_testing.app_b_py310.__file__).parent
    sys.path.append(str(testing_path))
    from docs_src.app_testing.app_b_py310 import test_main

    test_main.test_create_existing_item()
    test_main.test_create_item()
    test_main.test_create_item_bad_token()
    test_main.test_read_inexistent_item()
    test_main.test_read_item()
    test_main.test_read_item_bad_token()
    sys.path = current_path
