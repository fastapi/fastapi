from typing import Annotated, ForwardRef, get_args, get_origin

from fastapi import Depends, params
from fastapi.dependencies.utils import get_typed_annotation


def test_get_typed_annotation() -> None:
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    assert typed_annotation is None


def test_get_typed_annotation_falls_back_to_lenient_forwardref_resolution() -> None:
    def dependency() -> None:
        return None

    annotation = "Annotated[Potato, Depends(dependency)]"
    typed_annotation = get_typed_annotation(
        annotation,
        {"Annotated": Annotated, "Depends": Depends, "dependency": dependency},
    )

    assert get_origin(typed_annotation) is Annotated
    type_annotation, depends = get_args(typed_annotation)
    assert isinstance(type_annotation, ForwardRef)
    assert type_annotation.__forward_arg__ == "Potato"
    assert isinstance(depends, params.Depends)
