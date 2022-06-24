import functools

from fastapi import FastAPI

from .forward_reference_type import forwardref_method


def passthrough(f):
    @functools.wraps(f)
    def method(*args, **kwargs):
        return f(*args, **kwargs)

    return method


def test_wrapped_method_type_inference():
    """
    Regression test ensuring that when a method imported from another module
    is decorated with something that sets the __wrapped__ attribute, then
    the types are still processed correctly, including dereferencing of forward
    references.
    """
    app = FastAPI()
    app.get("/endpoint")(passthrough(forwardref_method))
    app.get("/endpoint2")(passthrough(passthrough(forwardref_method)))
