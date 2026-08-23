from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class HealthStatus(BaseModel):
    status: str


class ReadinessStatus(BaseModel):
    status: str
    database: bool


class AppState:
    def __init__(self) -> None:
        self.is_ready: bool = False
        self.db_healthy: bool = True


app_state = AppState()


async def check_database() -> bool:
    # In a real application, you would run a lightweight query (e.g. SELECT 1)
    return app_state.db_healthy


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Perform startup tasks (e.g. initialize connection pools, warm caches)
    app_state.is_ready = True
    yield
    # Perform shutdown cleanup
    app_state.is_ready = False


app = FastAPI(title="Kubernetes Probes Example", lifespan=lifespan)


@app.get(
    "/livez",
    tags=["health"],
    response_model=HealthStatus,
    summary="Liveness Probe",
)
async def liveness_probe() -> HealthStatus:
    """Check whether the application process is alive and responsive."""
    return HealthStatus(status="ok")


@app.get(
    "/readyz",
    tags=["health"],
    response_model=ReadinessStatus,
    summary="Readiness Probe",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Service Unavailable"}
    },
)
async def readiness_probe() -> ReadinessStatus:
    """Check whether the application and its dependencies are ready to accept traffic."""
    if not app_state.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application is still starting up",
        )

    db_ok = await check_database()
    if not db_ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is unhealthy",
        )

    return ReadinessStatus(status="ready", database=True)
