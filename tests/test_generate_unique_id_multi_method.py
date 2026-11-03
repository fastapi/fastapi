from fastapi import FastAPI
from fastapi.utils import generate_unique_id


class _ReversedIterationSet(set):
    """Methods whose iteration order does not start with the first name alphabetically."""

    def __iter__(self):
        return iter(sorted(super().__iter__(), reverse=True))


def test_generate_unique_id_ignores_the_set_iteration_order():
    app = FastAPI()

    @app.api_route("/x", methods=["GET", "POST"])
    def x():
        return None

    route = app.routes[-1]
    route.methods = _ReversedIterationSet({"GET", "POST"})

    # The id must come from the sorted methods, not from the set order.
    assert generate_unique_id(route) == "x_x_get"
