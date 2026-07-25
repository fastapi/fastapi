from fastapi.dependencies.models import Dependant, _get_oauth_scopes
from fastapi.dependencies.utils import get_flat_dependant, get_typed_annotation


def dependency_a() -> None:
    pass  # pragma: no cover


def dependency_b() -> None:
    pass  # pragma: no cover


def dependency_c() -> None:
    pass  # pragma: no cover


class UnhashableDependency:
    def __eq__(self, other: object) -> bool:
        return self is other

    def __call__(self) -> None:
        pass  # pragma: no cover


def test_get_typed_annotation() -> None:
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    assert typed_annotation is None


def test_get_flat_dependant_preserves_preorder_and_oauth_scopes() -> None:
    grandchild = Dependant(call=dependency_c, own_oauth_scopes=["grandchild"])
    child = Dependant(
        call=dependency_b,
        dependencies=[grandchild],
        own_oauth_scopes=["child"],
    )
    root = Dependant(
        call=dependency_a,
        dependencies=[child],
        own_oauth_scopes=["root"],
    )

    flat = get_flat_dependant(root)

    assert [dep.call for dep in flat.dependencies] == [
        dependency_b,
        dependency_c,
    ]
    assert _get_oauth_scopes(dependant=flat) == ["root"]
    assert _get_oauth_scopes(dependant=flat.dependencies[0]) == ["root", "child"]
    assert _get_oauth_scopes(dependant=flat.dependencies[1]) == [
        "root",
        "child",
        "grandchild",
    ]


def test_get_flat_dependant_skips_repeated_dependencies() -> None:
    shared = Dependant(call=dependency_c)
    root = Dependant(call=dependency_a, dependencies=[shared, shared])

    flat_with_repeats = get_flat_dependant(root)
    flat_without_repeats = get_flat_dependant(root, skip_repeats=True)

    assert [dep.call for dep in flat_with_repeats.dependencies] == [
        dependency_c,
        dependency_c,
    ]
    assert [dep.call for dep in flat_without_repeats.dependencies] == [dependency_c]


def test_get_flat_dependant_supports_unhashable_dependency_callables() -> None:
    dependency = UnhashableDependency()
    shared = Dependant(call=dependency)
    root = Dependant(call=dependency_a, dependencies=[shared, shared])

    flat = get_flat_dependant(root)
    flat_without_repeats = get_flat_dependant(root, skip_repeats=True)
    flat_with_existing_visited = get_flat_dependant(
        root,
        skip_repeats=True,
        visited=[(dependency, (), "")],
    )

    assert [dep.call for dep in flat.dependencies] == [dependency, dependency]
    assert [dep.call for dep in flat_without_repeats.dependencies] == [dependency]
    assert flat_with_existing_visited.dependencies == []


def test_get_flat_dependant_handles_deep_dependency_graph() -> None:
    root = Dependant(call=dependency_a)
    current = root
    for _ in range(500):
        child = Dependant(call=dependency_b)
        current.dependencies.append(child)
        current = child

    flat = get_flat_dependant(root)

    assert len(flat.dependencies) == 500
