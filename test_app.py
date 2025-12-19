from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI",
    description="""
## 🚀 Quick Start

```bash
curl -X GET http://127.0.0.1:8000/
""",
)


class HealthResponse(BaseModel):
    status: str


@app.get("/")
def root():
    return "Hello World"


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    tags=["System"],
)
def health_check():
    return HealthResponse(status="healthy")
