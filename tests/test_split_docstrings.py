from fastapi import FastAPI

app = FastAPI()


@app.get("/normal")
def doc_without_linefeed():
    """
    Normal doc without
    line feed.
    """


@app.get("/split")
def doc_with_linefeed():
    """
    Documentation that is broken appart
    \f
    by a line feed. This part should not appear in the description.
    """


def test_route_description_normal():
    found = False
    for route in app.routes:
        if route.path == "/normal":
            found = True
            assert (
                route.description
                == """Normal doc without
line feed."""
            )
    assert found, "Route was not found"


def test_route_description_split():
    found = False
    for route in app.routes:
        if route.path == "/split":
            found = True
            assert route.description == "Documentation that is broken appart\n"
    assert found, "Route was not found"
