from docs_src.python_types.tutorial010_py39 import Person, get_person_name


def test_get_person_name():
    assert get_person_name(Person("John Doe")) == "John Doe"
