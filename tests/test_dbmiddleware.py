import logging
from typing import List

import pytest
import sqlalchemy
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.database import transaction

from starlette.middleware.database import DatabaseMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

try:
    DATABASE_URL = 'postgresql://foo:bar@localhost/fastapi'
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

starlettenotes_fastapi = sqlalchemy.Table(
    "starlettenotes_fastapi",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


starlette = Starlette()
starlette.add_middleware(DatabaseMiddleware, database_url=DATABASE_URL, rollback_on_shutdown=True)

starlette_fastapi = FastAPI()
starlette_fastapi.add_middleware(DatabaseMiddleware, database_url=DATABASE_URL, rollback_on_shutdown=True)

fastapi = FastAPI()
fastapi.add_middleware(
    DatabaseMiddleware, database_url=DATABASE_URL, rollback_on_shutdown=True
)


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    engine.execute("DROP TABLE fastapinotes")
    engine.execute("DROP TABLE starlettenotes")
    engine.execute("DROP TABLE starlettenotes_fastapi")


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
async def add_note_fastapi(note: NoteIn, raise_exc: bool = False):
    """
    Create a note: FastAPI style
    """
    query = fastapinotes.insert().values(text=note.text, completed=note.completed)
    async with fastapi.error_middleware.app.backend.session().transaction():
        if raise_exc:
            raise RuntimeError()
        await fastapi.error_middleware.app.backend.session().execute(query)
    return note


@starlette.route("/notes_starlette", methods=["POST"])
@transaction
async def add_note_starlette(request):
    """
    Create a note: Starlette style
    """
    data = await request.json()
    query = starlettenotes.insert().values(text=data["text"], completed=data["completed"])
    await request.database.execute(query)
    if "raise_exc" in request.query_params:
        raise RuntimeError()
    return JSONResponse({"text": data["text"], "completed": data["completed"]})


@starlette_fastapi.route("/notes_starlette", methods=["POST"])
@transaction
async def add_note_starlette(request):
    """
    Create a note: Starlette style with FastAPI
    """
    data = await request.json()
    query = starlettenotes_fastapi.insert().values(text=data["text"], completed=data["completed"])
    await request.database.execute(query)
    if "raise_exc" in request.query_params:
        raise RuntimeError()
    return JSONResponse({"text": data["text"], "completed": data["completed"]})


@fastapi.get("/notes", response_model=List[NoteOut])
async def list_notes_fastapi():
    """
    Get all notes: FastAPI style
    """
    query = fastapinotes.select()
    results = await fastapi.error_middleware.app.backend.session().fetchall(query)
    return results


@starlette.route("/notes_starlette", methods=["GET"])
async def list_notes_starlette(request):
    """
    Get all notes: Starlette style
    """
    query = starlettenotes.select()
    results = await request.database.fetchall(query)
    content = [
        {"text": result["text"], "completed": result["completed"]} for result in results
    ]
    return JSONResponse(content)


@starlette_fastapi.route("/notes_starlette", methods=["GET"])
async def list_notes_starlette(request):
    """
    Get all notes: Starlette style with FastAPI
    """
    query = starlettenotes_fastapi.select()
    results = await request.database.fetchall(query)
    content = [
        {"text": result["text"], "completed": result["completed"]} for result in results
    ]
    return JSONResponse(content)


@fastapi.post("/notes/bulk_create")
async def bulk_create_notes_fastapi(notelist: List[dict]):
    """
    Create notes in bulk: FastAPI style
    """
    query = fastapinotes.insert()
    await fastapi.error_middleware.app.backend.session().executemany(query, notelist)
    return notelist


@starlette.route("/notes_starlette/bulk_create", methods=["POST"])
async def bulk_create_notes_starlette(request):
    """
    Create notes in bulk: Starlette style
    """
    data = await request.json()
    query = starlettenotes.insert()
    await request.database.executemany(query, data)
    return JSONResponse({"notes": data})


@starlette_fastapi.route("/notes_starlette/bulk_create", methods=["POST"])
async def bulk_create_notes_starlette(request):
    """
    Create notes in bulk: Starlette style with FastAPI
    """
    data = await request.json()
    query = starlettenotes_fastapi.insert()
    await request.database.executemany(query, data)
    return JSONResponse({"notes": data})

@fastapi.get("/notes/{note_id}", response_model=NoteOut)
async def read_note_fastapi_starlette(note_id: int):
    """
    Get a note by id: FastAPI
    """
    query = fastapinotes.select().where(fastapinotes.c.id == note_id)
    result = await fastapi.error_middleware.app.backend.session().fetchone(query)
    logger.debug('result')
    logger.debug(result)
    return result


@starlette.route("/notes_starlette/{note_id:int}", methods=["GET"])
async def read_note_starlette(request):
    """
    Get a note by id: Starlette
    """
    note_id = request.path_params["note_id"]
    query = starlettenotes.select().where(starlettenotes.c.id == note_id)
    result = await request.database.fetchone(query)
    content = {"text": result["text"], "completed": result["completed"]}
    return JSONResponse(content)


@starlette_fastapi.route("/notes_starlette/{note_id:int}", methods=["GET"])
async def read_note_starlette(request):
    """
    Get a note by id: Starlette with FastAPI
    """
    note_id = request.path_params["note_id"]
    query = starlettenotes_fastapi.select().where(starlettenotes_fastapi.c.id == note_id)
    result = await request.database.fetchone(query)
    content = {"text": result["text"], "completed": result["completed"]}
    return JSONResponse(content)


@fastapi.get("/notes/{note_id}/text")
async def read_note_text_fastapi(note_id: int):
    """
    Get the text of a note by id: FastAPI
    """
    query = sqlalchemy.select([fastapinotes.c.text]).where(fastapinotes.c.id == note_id)
    text = await fastapi.error_middleware.app.backend.session().fetchval(query)
    return text


@starlette.route("/notes_starlette/{note_id:int}/text", methods=["GET"])
async def read_note_text_starlette(request):
    """
    Get the text of a note by id: Starlette
    """
    note_id = request.path_params["note_id"]
    query = sqlalchemy.select([starlettenotes.c.text]).where(starlettenotes.c.id == note_id)
    text = await request.database.fetchval(query)
    return JSONResponse(text)


@starlette_fastapi.route("/notes_starlette/{note_id:int}/text", methods=["GET"])
async def read_note_text_starlette(request):
    """
    Get the text of a note by id: Starlette with FastAPI
    """
    note_id = request.path_params["note_id"]
    query = sqlalchemy.select([starlettenotes_fastapi.c.text]).where(starlettenotes_fastapi.c.id == note_id)
    text = await request.database.fetchval(query)
    return JSONResponse(text)


class TestStarletteStyleWithFastAPI():

    def test_database(self):
        with TestClient(starlette_fastapi) as client:
            response = client.post(
                "/notes_starlette", json={"text": "buy the milk", "completed": True}
            )
            assert response.status_code == 200

            with pytest.raises(RuntimeError):
                response = client.post(
                    "/notes_starlette",
                    json={"text": "you wont see me", "completed": False},
                    params={"raise_exc": "true"},
                )

            response = client.post(
                "/notes_starlette", json={"text": "walk the dog", "completed": False}
            )
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

            response = client.get("/notes_starlette/1")
            assert response.status_code == 200
            assert response.json() == {"text": "buy the milk", "completed": True}

            response = client.get("/notes_starlette/1/text")
            assert response.status_code == 200
            assert response.json() == "buy the milk"

    def test_database_executemany(self):
        with TestClient(starlette_fastapi) as client:
            data = [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]
            response = client.post("/notes_starlette/bulk_create", json=data)
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

    def test_database_isolated_during_test_cases(self):
        """
        Using `TestClient` as a context manager
        """

        with TestClient(starlette_fastapi) as client:
            response = client.post(
                "/notes_starlette", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]

        with TestClient(starlette_fastapi) as client:
            response = client.post(
                "/notes_starlette", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]


class TestStarletteStyle():

    def test_database(self):
        with TestClient(starlette) as client:
            response = client.post(
                "/notes_starlette", json={"text": "buy the milk", "completed": True}
            )
            assert response.status_code == 200

            with pytest.raises(RuntimeError):
                response = client.post(
                    "/notes_starlette",
                    json={"text": "you wont see me", "completed": False},
                    params={"raise_exc": "true"},
                )

            response = client.post(
                "/notes_starlette", json={"text": "walk the dog", "completed": False}
            )
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

            response = client.get("/notes_starlette/1")
            assert response.status_code == 200
            assert response.json() == {"text": "buy the milk", "completed": True}

            response = client.get("/notes_starlette/1/text")
            assert response.status_code == 200
            assert response.json() == "buy the milk"

    def test_database_executemany(self):
        with TestClient(starlette) as client:
            data = [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]
            response = client.post("/notes_starlette/bulk_create", json=data)
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [
                {"text": "buy the milk", "completed": True},
                {"text": "walk the dog", "completed": False},
            ]

    def test_database_isolated_during_test_cases(self):
        """
        Using `TestClient` as a context manager
        """

        with TestClient(starlette) as client:
            response = client.post(
                "/notes_starlette", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]

        with TestClient(starlette) as client:
            response = client.post(
                "/notes_starlette", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes_starlette")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]


class TestFastAPIStyle():

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
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]

        with TestClient(client) as client:
            response = client.post(
                "/notes", json={"text": "just one note", "completed": True}
            )
            assert response.status_code == 200

            response = client.get("/notes")
            assert response.status_code == 200
            assert response.json() == [{"text": "just one note", "completed": True}]
