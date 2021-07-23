from typing import AsyncGenerator, List

import databases
import sqlalchemy
from fastapi import Depends, FastAPI
from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    db_url: str


def get_config() -> Settings:
    return Settings()


metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


def setup_schema(config: Settings = Depends(get_config)) -> None:
    engine = sqlalchemy.create_engine(
        config.db_url, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)


async def get_db(
    config: Settings = Depends(get_config), schema: None = Depends(setup_schema)
) -> AsyncGenerator[databases.Database, None]:
    async with databases.Database(config.db_url) as db:
        yield db


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


async def startup(
    db: databases.Database = Depends(get_db, use_cache="app", lifetime="app")
):
    db.execute("SELECT 1")  # checks that we are properly connected to the database


app = FastAPI(on_startup=[startup])


@app.get("/notes/", response_model=List[Note])
async def read_notes(db: databases.Database = Depends(get_db)):
    query = notes.select()
    return await db.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn, db: databases.Database = Depends(get_db)):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await db.execute(query)
    return {**note.dict(), "id": last_record_id}
