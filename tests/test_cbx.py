from fastapi import APIRouter
from fastapi.cbx import cbr, cbv


def test_cbv_all():
    router = APIRouter()

    @cbv(router)
    class Test:
        test_attr = 1

        def get(self):
            pass

        def post(self):
            pass

        def put(self):
            pass

        def delete(self):
            pass

        def head(self):
            pass

        def patch(self):
            pass

        def options(self):
            pass

        def trace(self):
            pass

        def connect(self):
            pass

    Test.test_attr
    dir(Test)
    Test()


def test_cbr_all():
    router = APIRouter()

    @cbr(router)
    class Test:
        test_attr = 1

        @cbr.get("/g")
        def g(self):
            pass

        @cbr.post("/p")
        def p(self):
            pass

        @cbr.put("/u")
        def u(self):
            pass

        @cbr.delete("/d")
        def d(self):
            pass

        @cbr.head("/h")
        def h(self):
            pass

        @cbr.patch("/pt")
        def pt(self):
            pass

        @cbr.options("/o")
        def o(self):
            pass

        @cbr.trace("/t")
        def t(self):
            pass

        @cbr.connect("/c")
        def c(self):
            pass

        @cbr.get("/1")
        @cbr.get("/2")
        def multi(self):
            pass

    Test.test_attr
    dir(Test)
    Test()
