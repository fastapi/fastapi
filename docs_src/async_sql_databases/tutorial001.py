from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(NoteIn):
    id: int


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.get("/notes/{note_id}/", response_model=Note)
async def read_one_note(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    note = await database.fetch_one(query)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(**note.dict())
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


@app.put("/notes/{note_id}/")
async def update_note(note_id: int, note: NoteIn):
    query = notes.select().where(notes.c.id == note_id)
    note_fetched = await database.fetch_one(query)
    if note_fetched is None:
        raise HTTPException(status_code=404, detail="Note not found")
    query = notes.update().values(**note.dict()).where(notes.c.id == note_id)
    await database.execute(query)


@app.delete("/notes/{note_id}/")
async def delete_note(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    note = await database.fetch_one(query)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
