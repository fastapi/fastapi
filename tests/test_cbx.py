import asyncio
import logging

from fastapi import APIRouter, Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.cbx import cbr, cbv
from fastapi.testclient import TestClient
from pydantic import BaseModel


@cbv(router=APIRouter(prefix="/cbv"))
class MyCBV:
    logger = logging.getLogger(__qualname__)

    class CBVModel(BaseModel):
        key: str = "cbv"
        value: str = "Class-based view for CRUD operations with singleton global dependency injection"

    def __init__(self, **kwargs: dict[str, str]):
        self.heavies = {
            "name": "fastapi-cbx",
            "description": "Minimal class-based routing extension for FastAPI",
            "requires-python": ">=3.8",
        }
        self.heavies.update(kwargs)

    @staticmethod
    async def head(response: Response) -> None:
        await asyncio.sleep(1)
        response.status_code = status.HTTP_200_OK
        response.set_cookie("token", "fastapi-cbx")

    async def get(self, key: str) -> CBVModel:
        self.logger.info(f"GET {key}")
        await asyncio.sleep(1)
        return self.CBVModel(
            key=key, value=self.heavies.get(key, "One scenario, one route")
        )


@cbr(router=APIRouter(prefix="/cbr"))
class MyCBR:
    logger = logging.getLogger(__qualname__)

    class CBRModel(BaseModel):
        key: str = "CBR"
        value: str = "Class-based route for complex business logic with multiple endpoints and method-level dependencies"

    def __init__(self, **kwargs: dict[str, str]):
        self.heavies = {
            "name": "fastapi-cbx",
            "description": "Minimal class-based routing extension for FastAPI",
        }
        self.heavies.update(kwargs)

    @cbr.get("/welcome", summary="Welcome to fastapi-cbx")
    @staticmethod
    async def welcome(response: Response) -> str:
        response.status_code = status.HTTP_200_OK
        response.set_cookie("token", "fastapi-cbx")
        return "Welcome to fastapi-cbx"

    @cbr.get("/heavies", summary="Get heavies by key")
    async def get_heavies(self, key: str) -> CBRModel:
        self.logger.info(f"GET {key}")
        return self.CBRModel(
            key=key, value=self.heavies.get(key, "One scenario, one route")
        )

    @staticmethod
    def session(token: str = Cookie(default="", alias="token")) -> str:
        if token != "fastapi-cbx":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return token

    @cbr.post("/heavies", summary="Set heavies")
    @cbr.put("/heavies", summary="Set heavies")
    @cbr.patch("/heavies", summary="Set heavies")
    async def set_heavies(self, body: CBRModel, token: str = Depends(session)) -> None:
        self.logger.info(f"POST {body.key} {body.value} {token}")
        await asyncio.sleep(1)
        self.heavies[body.key] = body.value

    @cbr.delete("/heavies")
    async def delete(self, name: str) -> None:
        del self.heavies[name]

    @cbr.head("/multiple_coverage")
    @cbr.options("/multiple_coverage")
    @cbr.trace("/multiple_coverage")
    @cbr.connect("/multiple_coverage")
    @staticmethod
    async def multiple_coverage(response: Response) -> None:
        response.status_code = status.HTTP_200_OK
        response.set_cookie("token", "fastapi-cbx")


MyCBV(version="1.0.0")
MyCBR(version="1.0.0")
app = FastAPI()

app.include_router(MyCBV.router)
app.include_router(MyCBR.router)

client = TestClient(app)


# ==================== 100% Test Suite ====================


def test_cbv():
    asyncio.run(MyCBV.head(Response()))
    print(dir(MyCBV))
    response = client.get("/cbv?key=name")
    assert response.status_code == 200


def test_cbr():
    asyncio.run(MyCBR.welcome(Response()))
    print(dir(MyCBR))
    response = client.get("/cbr/heavies?key=name")
    assert response.status_code == 200
    response = client.post("/cbr/heavies", json={"key": "test", "value": "test_value"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

    with TestClient(app, cookies={"token": "fastapi-cbx"}) as auth_client:
        response = auth_client.post(
            "/cbr/heavies", json={"key": "test", "value": "test"}
        )
        assert response.status_code == 200
    response = client.delete("/cbr/heavies?name=test")
    assert response.status_code == 200
    response = client.head("/cbr/multiple_coverage")
    assert response.status_code == 200
