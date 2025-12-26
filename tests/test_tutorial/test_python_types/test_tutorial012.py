from docs_src.python_types.tutorial012_py39 import User


def test_user():
    user = User(name="John Doe", age=30)
    assert user.name == "John Doe"
    assert user.age == 30
