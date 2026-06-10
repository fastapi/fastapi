from fastapi.dependencies.utils import _version_str_to_tuple, get_typed_annotation


def test_version_str_to_tuple():
    assert _version_str_to_tuple("0.0.12") == (0, 0, 12)
    assert _version_str_to_tuple("0.0.100") == (0, 0, 100)
    assert _version_str_to_tuple("1.2.3a1") == (1, 2, 3)
    assert _version_str_to_tuple("") == ()


def test_get_typed_annotation():
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    assert typed_annotation is None
