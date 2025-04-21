import asyncio
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, FastAPI
from fastapi.params import Depends
from fastapi.responses import PlainTextResponse


@lru_cache
@dataclass
class ClientSettings:
    timeout: int


@dataclass
class Client(ABC):
    settings: ClientSettings

    async def _connect(self):
        await asyncio.sleep(min(random.randint(1, 5), self.settings.timeout))

    @abstractmethod
    async def request(self) -> str:
        raise NotImplementedError


class CityClient(Client):
    async def request(self) -> str:
        await self._connect()

        return "Response"


class VillageClient(Client):
    @staticmethod
    def _get_ip() -> str:
        return "127.0.0.1"

    async def request(self) -> str:
        ip = self._get_ip()
        await self._connect()

        return f"Response, {ip}"


def get_client_settings() -> ClientSettings:
    return ClientSettings(timeout=3)


ClientSettingsDep = Annotated[ClientSettings, Depends(get_client_settings)]


def get_city_client(settings: ClientSettingsDep) -> CityClient:
    return CityClient(settings=settings)


CityClientDep = Annotated[CityClient, Depends(get_city_client)]


def get_village_client(settings: ClientSettingsDep) -> VillageClient:
    return VillageClient(settings=settings)


VillageClientDep = Annotated[VillageClient, Depends(get_village_client)]


geo_router = APIRouter(prefix="/geo", tags=["Geo"])


@geo_router.get(
    "",
    response_class=PlainTextResponse,
    summary="Fetches geodata.",
)
async def get(client: CityClientDep) -> str:
    return await client.request()


def main() -> FastAPI:
    app = FastAPI(title="DI != DI")

    for router in (geo_router,):
        app.include_router(router, prefix="/api")

    return app
