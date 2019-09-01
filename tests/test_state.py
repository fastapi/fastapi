from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient


def test_state_data_across_multiple_middlewares():
    expected_value1 = "foo"
    expected_value2 = "bar"

    class aMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            request.state.foo = expected_value1
            response = await call_next(request)
            return response

    class bMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            request.state.bar = expected_value2
            response = await call_next(request)
            response.headers["X-State-Foo"] = request.state.foo
            return response

    class cMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)
            response.headers["X-State-Bar"] = request.state.bar
            return response

    app = FastAPI()
    app.add_middleware(aMiddleware)
    app.add_middleware(bMiddleware)
    app.add_middleware(cMiddleware)

    @app.get("/")
    def homepage():
        return PlainTextResponse("OK")

    client = TestClient(app)
    response = client.get("/")
    assert response.text == "OK"
    assert response.headers["X-State-Foo"] == expected_value1
    assert response.headers["X-State-Bar"] == expected_value2


class SomeService(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.total = None

    def startup(self):
        self.total = self.a + self.b

    def shutdown(self):
        self.total = 0


app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    service = SomeService(a=1, b=2)
    service.startup()
    app.state.service = service


@app.on_event("shutdown")
async def shutdown():
    service = app.state.service
    service.shutdown()


@app.get("/")
def homepage():
    return {"ok"}


def test_state_across_events():
    with TestClient(app) as client:
        assert app.state.service.total == 3
        response = client.get("/")
        assert response.status_code == 200
    assert app.state.service.total == 0
