import asyncio
import random
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated

from dishka import (
    FromDishka,
    Provider,
    Scope,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import DishkaRoute, setup_dishka
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import PlainTextResponse


@dataclass
class User:
    name: str = "Pythonist"
    email: str = "python@example.com"


@dataclass
class ClientSettings:
    user: User

    timeout: int = 3
    retries: int = 5


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

        return f"Hello, dear {self.settings.user.name}! Response"


@dataclass
class VillageClient(Client):
    ip: str = "192.168.0.1"

    async def request(self) -> str:
        await self._connect()

        return f"Hello, {self.settings.user.name}! Response, {self.ip}"


class GeoProvider(Provider):
    scope = Scope.APP

    provides = provide(
        source=CityClient,
        scope=Scope.REQUEST,
        provides=Client,
        recursive=True,
    )


geo_router = APIRouter(
    prefix="/geo",
    tags=["Geo"],
    route_class=DishkaRoute,
)


async def get_metadata(request: Request) -> str:
    metadata = request.headers.get("User-Agent", default="")
    return f"Trace from the Browser wars: {metadata}"


@geo_router.get(
    "",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata.",
)
async def get(
    client: FromDishka[Client],
) -> str:
    return await client.request()


@geo_router.get(
    "/extended",
    response_class=PlainTextResponse,
    summary="Fetches and returns geodata with user's metadata.",
)
async def get_extended(
    metadata: Annotated[str, Depends(get_metadata)],
    client: FromDishka[Client],
) -> str:
    geodata = await client.request()

    return f"{geodata}. {metadata}."


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await app.state.dishka_container.close()


def main() -> FastAPI:
    app = FastAPI(
        title="Dishka is rushing to the rescue",
        lifespan=lifespan,
    )

    for router in (geo_router,):
        app.include_router(router, prefix="/api")

    container = make_async_container(GeoProvider())
    setup_dishka(container, app)

    return app
