import asyncio
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import PlainTextResponse


@lru_cache
@dataclass
class User:
    name: str = "Pythonist"
    email: str = "python@example.com"


UserDep = Annotated[User, Depends(User)]


@lru_cache
@dataclass
class ClientSettings:
    user: UserDep

    timeout: int = 3
    retries: int = 5


ClientSettingsDep = Annotated[ClientSettings, Depends(ClientSettings)]


@dataclass
class Client(ABC):
    settings: ClientSettingsDep

    async def _connect(self):
        for _ in range(self.settings.retries):
            if random.choice((True, False)):
                reply_time = random.randint(1, 5)
                await asyncio.sleep(min(reply_time, self.settings.timeout))

                return

    @abstractmethod
    async def request(self) -> str:
        raise NotImplementedError


class CityClient(Client):
    async def request(self) -> str:
        await self._connect()

        return f"Hello, dear {self.settings.user.name}! Response"


@dataclass
class VillageClient(Client):
    ip: str = "192.168.0.1"

    async def request(self) -> str:
        await self._connect()

        return f"Hello, {self.settings.user.name}! Response, {self.ip}"


CityClientDep = Annotated[Client, Depends(CityClient)]

VillageClientDep = Annotated[Client, Depends(VillageClient)]

ClientDep = CityClientDep

geo_router = APIRouter(prefix="/geo", tags=["Geo"])


@geo_router.get(
    "",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata.",
)
async def get(
    client: ClientDep,
) -> str:
    return await client.request()


@geo_router.get(
    "/extended",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata with user's metadata.",
)
async def get_extended(
    request: Request,
    client: ClientDep,
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
