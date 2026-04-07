from docs_src.app_testing import tutorial003, tutorial003_py310


def test_tutorial003():
    # This covers the base version (tutorial003.py)
    tutorial003.test_read_items()


def test_tutorial003_py310():
    # This covers the modern version (tutorial003_py310.py)
    tutorial003_py310.test_read_items()
