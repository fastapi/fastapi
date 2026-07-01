import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


# Custom filter to remove healthcheck endpoints from logs
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.args and len(record.args) >= 3:
            path = record.args[2]
            if path in ("/healthz", "/readyz", "/livez"):
                return False
        return True


# Apply the filter to the uvicorn.access logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup operations (e.g. database connections) here
    yield
    # Perform cleanup operations here


app = FastAPI(lifespan=lifespan)


@app.get("/healthz")
def healthz():
    """Liveness probe endpoint."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    """Readiness probe endpoint."""
    # You could also check database connectivity here
    return {"status": "ready"}
