from docs_src.python_types.tutorial013 import say_hello


def test_say_hello():
    assert say_hello("FastAPI") == "Hello FastAPI"
