import asyncio
import random
from abc import ABC, abstractmethod

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import PlainTextResponse


class Client(ABC):
    timeout = 3

    async def _connect(self):
        await asyncio.sleep(min(random.randint(1, 5), self.timeout))

    @abstractmethod
    async def request(self) -> str:
        raise NotImplementedError


class CityClient(Client):
    async def request(self) -> str:
        await self._connect()

        return "Response"


class VillageClient(Client):
    ip = "192.168.0.1"

    async def request(self) -> str:
        await self._connect()

        return f"Response, {self.ip}"


CurrentClient = CityClient


geo_router = APIRouter(prefix="/geo", tags=["Geo"])


@geo_router.get(
    "",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata.",
)
async def get(
    client: Client = Depends(CurrentClient),
) -> str:
    return await client.request()


@geo_router.get(
    "/extended",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata with user's metadata.",
)
async def get_extended(
    request: Request,
    client: Client = Depends(CurrentClient),
) -> str:
    geodata = await client.request()

    metadata = request.headers.get("User-Agent", default="")
    return f"{geodata}. Trace from the Browser wars: {metadata}."


def main() -> FastAPI:
    app = FastAPI(
        title="Depends is rushing to the rescue",
    )

    for router in (geo_router,):
        app.include_router(router, prefix="/api")

    return app
