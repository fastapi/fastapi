from fastapi.dependencies.utils import get_typed_annotation


def test_get_typed_annotation():
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    assert typed_annotation is None
