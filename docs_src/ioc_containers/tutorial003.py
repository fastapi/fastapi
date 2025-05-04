import asyncio
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import PlainTextResponse


class User:
    name = "Pythonist"
    email = "python@example.com"


@lru_cache
def get_user() -> User:
    return User()


@dataclass
class ClientSettings:
    user: User

    timeout = 3
    retries = 5


@lru_cache
def get_client_settings(user: User = Depends(get_user)) -> ClientSettings:
    return ClientSettings(user=user)


@dataclass
class Client(ABC):
    settings: ClientSettings

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

        return f"Hello, {self.settings.user.name}! Response"


class VillageClient(Client):
    ip = "192.168.0.1"

    async def request(self) -> str:
        await self._connect()

        return f"Hello, {self.settings.user.name}! Response, {self.ip}"


async def get_city_client(
    settings: ClientSettings = Depends(get_client_settings),
) -> Client:
    return CityClient(settings=settings)


async def get_village_client(
    settings: ClientSettings = Depends(get_client_settings),
) -> Client:
    return VillageClient(settings=settings)


get_client = get_city_client

geo_router = APIRouter(prefix="/geo", tags=["Geo"])


@geo_router.get(
    "",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata.",
)
async def get(
    client: Client = Depends(get_client),
) -> str:
    return await client.request()


@geo_router.get(
    "/extended",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata with user's metadata.",
)
async def get_extended(
    request: Request,
    client: Client = Depends(get_client),
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
