import logging
from typing import List

import pytest
import sqlalchemy
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.database import transaction
from starlette.middleware.database import DatabaseMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# docker run --name fastapi-postgres -e POSTGRES_PASSWORD=bar -e POSTGRES_USER=foo -e POSTGRES_DB=fastapi -p 5432:5432 -d postgres
try:
    DATABASE_URL = "postgresql://foo:bar@localhost/fastapi"
except KeyError:  # pragma: no cover
    pytest.skip("DATABASE_URL is not set", allow_module_level=True)

metadata = sqlalchemy.MetaData()

fastapinotes = sqlalchemy.Table(
    "fastapinotes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

starlettenotes = sqlalchemy.Table(
    "starlettenotes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


fastapi = FastAPI()
fastapi.add_middleware(
    DatabaseMiddleware, database_url=DATABASE_URL, rollback_on_shutdown=True
)


@pytest.fixture(autouse=True, scope="function")
def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    engine.execute("DROP TABLE fastapinotes")
    engine.execute("DROP TABLE starlettenotes")


class NoteIn(BaseModel):
    text: str
    completed: bool


class NoteOut(BaseModel):
    text: str
    completed: bool


class NoteOutJustText(BaseModel):
    text: str


class NoteDB(BaseModel):
    id: int
    text: str
    completed: bool


@fastapi.post("/notes")
async def add_note_fastapi(request: Request, note: NoteIn):
    """
    Create a note: FastAPI style
    """
    query = fastapinotes.insert().values(text=note.text, completed=note.completed)
    async with request.database.transaction():
        await request.database.execute(query)
        if "raise_exc" in request.query_params:
            raise RuntimeError()
    return note


@fastapi.get("/notes", response_model=List[NoteOut])
async def list_notes_fastapi(request: Request):
    """
    Get all notes: FastAPI style
    """
    query = fastapinotes.select()
    results = await request.database.fetchall(query)
    return results


@fastapi.post("/notes/bulk_create")
async def bulk_create_notes_fastapi(request: Request, notelist: List[NoteIn]):
    """
    Create notes in bulk: FastAPI style
    """
    query = fastapinotes.insert()
    await request.database.executemany(query, [n.dict() for n in notelist])
    return notelist


@fastapi.get("/notes/{note_id}", response_model=NoteOut)
async def read_note_fastapi_starlette(request: Request, note_id: int):
    """
    Get a note by id: FastAPI
    """
    query = fastapinotes.select().where(fastapinotes.c.id == note_id)
    result = await request.database.fetchone(query)
    logger.debug("result")
    logger.debug(result)
    return result


@fastapi.get("/notes/{note_id}/text")
async def read_note_text_fastapi(request: Request, note_id: int):
    """
    Get the text of a note by id: FastAPI
    """
    query = sqlalchemy.select([fastapinotes.c.text]).where(fastapinotes.c.id == note_id)
    text = await request.database.fetchval(query)
    return text


class TestFastAPIStyle:
    def test_database(self):
        with TestClient(fastapi) as client:
            response = client.post(
                "/notes", json={"text": "buy the milk", "completed": True}
            )
            assert response.status_code == 200

            with pytest.raises(RuntimeError):
                response = client.post(
                    "/notes",
                    json={"text": "you wont see me", "completed": False},
                    params={"raise_exc": "true"},
                )

            response = client.post(
                "/notes", json={"text": "walk the dog", "completed": False}
            )
            assert response.status_code == 200

            response = client.get("/notes")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

            response = client.get("/notes/1")
            assert response.status_code == 200
            assert response.json() == {"text": "buy the milk", "completed": True}

            response = client.get("/notes/1/text")
            assert response.status_code == 200
            assert response.json() == "buy the milk"

    def test_database_executemany(self):
        with TestClient(fastapi) as client:
            data = [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]
            response = client.post("/notes/bulk_create", json=data)
            assert response.status_code == 200

            response = client.get("/notes")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

    def test_database_isolated_during_test_cases(self):
        """
        Using `TestClient` as a context manager
        """

        with TestClient(fastapi) as client:
            response = client.post(
                "/notes", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes")
            logger.debug(response.json())
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]

        with TestClient(fastapi) as client:
            response = client.post(
                "/notes", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]


@pytest.fixture(params=["fastapistarlette", "starlette"])
def framework(request):
    if request.param == "fastapistarlette":
        app = FastAPI()
    else:
        app = Starlette()
    app.add_route("/notes", add_note_s, methods=["POST"])
    app.add_route("/notes", list_notes_s, methods=["GET"])
    app.add_route("/notes/{note_id:int}", read_note_s, methods=["GET"])
    app.add_route("/notes/{note_id:int}/text", read_note_text_s, methods=["GET"])
    app.add_route("/notes/bulk_create", bulk_create_notes_s, methods=["POST"])
    app.add_middleware(
        DatabaseMiddleware, database_url=DATABASE_URL, rollback_on_shutdown=True
    )
    yield app


@transaction
async def add_note_s(request):
    """
    Create a note: Starlette style
    """
    data = await request.json()
    query = starlettenotes.insert().values(
        text=data["text"], completed=data["completed"]
    )
    await request.database.execute(query)
    if "raise_exc" in request.query_params:
        raise RuntimeError()
    return JSONResponse({"text": data["text"], "completed": data["completed"]})


async def list_notes_s(request):
    """
    Get all notes: Starlette style
    """
    query = starlettenotes.select()
    results = await request.database.fetchall(query)
    content = [
        {"text": result["text"], "completed": result["completed"]} for result in results
    ]
    return JSONResponse(content)


async def read_note_s(request):
    """
    Get a note by id: Starlette
    """
    note_id = request.path_params["note_id"]
    query = starlettenotes.select().where(starlettenotes.c.id == note_id)
    result = await request.database.fetchone(query)
    content = {"text": result["text"], "completed": result["completed"]}
    return JSONResponse(content)


async def read_note_text_s(request):
    """
    Get the text of a note by id: Starlette
    """
    note_id = request.path_params["note_id"]
    query = sqlalchemy.select([starlettenotes.c.text]).where(
        starlettenotes.c.id == note_id
    )
    text = await request.database.fetchval(query)
    return JSONResponse(text)


async def bulk_create_notes_s(request):
    """
    Create notes in bulk: Starlette style
    """
    data = await request.json()
    query = starlettenotes.insert()
    await request.database.executemany(query, data)
    return JSONResponse({"notes": data})


@pytest.fixture
def frameworkclient(framework):
    yield TestClient(framework)


class TestStarletteStyle(object):
    def test_database(self, frameworkclient):
        with frameworkclient:
            response = frameworkclient.post(
                "/notes", json={"text": "buy the milk", "completed": True}
            )
            assert response.status_code == 200

            with pytest.raises(RuntimeError):
                response = frameworkclient.post(
                    "/notes",
                    json={"text": "you wont see me", "completed": False},
                    params={"raise_exc": "true"},
                )

            response = frameworkclient.post(
                "/notes", json={"text": "walk the dog", "completed": False}
            )
            assert response.status_code == 200

            response = frameworkclient.get("/notes")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

            response = frameworkclient.get("/notes/1")
            assert response.status_code == 200
            assert response.json() == {"text": "buy the milk", "completed": True}

            response = frameworkclient.get("/notes/1/text")
            assert response.status_code == 200
            assert response.json() == "buy the milk"

    def test_database_executemany(self, frameworkclient):
        with frameworkclient:
            data = [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]
            response = frameworkclient.post("/notes/bulk_create", json=data)
            assert response.status_code == 200

            response = frameworkclient.get("/notes")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

    def test_database_isolated_during_test_cases(self, frameworkclient):
        """
        Using `TestClient` as a context manager
        """

        with frameworkclient:
            response = frameworkclient.post(
                "/notes", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = frameworkclient.get("/notes")
            logger.debug(response.json())
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]

        with frameworkclient:
            response = frameworkclient.post(
                "/notes", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = frameworkclient.get("/notes")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]
