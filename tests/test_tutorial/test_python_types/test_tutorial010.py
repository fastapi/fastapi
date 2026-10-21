from docs_src.python_types.tutorial010_py310 import Person, get_person_name


def test_get_person_name():
    assert get_person_name(Person("John Doe")) == "John Doe"
