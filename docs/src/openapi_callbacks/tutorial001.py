import json

from fastapi import APIRouter, FastAPI
from pydantic import UUID4, BaseModel, UrlStr
from starlette.responses import JSONResponse

app = FastAPI()

# Model definitions
class HealthResponse(BaseModel):
    status: str


class HealthRequest(BaseModel):
    endpoint_name: str


class ClientInfo(BaseModel):
    name: str
    health: UrlStr = None


class ClientAddedResponse(BaseModel):
    id: UUID4


cb_router = APIRouter()


@callback_router.get(
    "{$request.body.health}",
    name="health",
    response_model=HealthResponse,
    response_class=JSONResponse,
)
async def health(endpoint: str):
    return {"status": f"{endpoint} ok"}


@app.post("/clients/", response_model=ClientAddedResponse, callbacks=cb_router.routes)
async def register_client(client_info: ClientInfo):
    pass

