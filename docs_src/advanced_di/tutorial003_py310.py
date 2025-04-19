import asyncio
import random
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from dishka import (
    FromDishka,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import DishkaRoute, setup_dishka
from fastapi import APIRouter, FastAPI
from fastapi.responses import PlainTextResponse


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


class GeoProvider(Provider):
    scope = Scope.REQUEST

    provides = from_context(provides=ClientSettings, scope=Scope.APP) + provide(
        source=CityClient, provides=Client
    )


geo_router = APIRouter(prefix="/geo", tags=["Geo"], route_class=DishkaRoute)


@geo_router.post(
    "",
    response_class=PlainTextResponse,
    summary="Fetches geodata.",
)
async def create(client: FromDishka[Client]) -> str:
    return await client.request()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await app.state.dishka_container.close()


def main() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    for router in (geo_router,):
        app.include_router(router, prefix="/api")

    container = make_async_container(
        GeoProvider(), context={ClientSettings: ClientSettings(timeout=3)}
    )
    setup_dishka(container, app)

    return app
