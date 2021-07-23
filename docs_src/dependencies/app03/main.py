from typing import List

from databases import Database
from fastapi import Depends, FastAPI
from fastapi.dependencies.lifetime import DependencyLifetime

from .db import get_db
from .models import Note, NoteIn
from .schemas import notes

app = FastAPI()


@app.on_event("startup")
async def startup(db: Database = Depends(get_db, lifetime=DependencyLifetime.app)):
    db.execute("SELECT 1")  # checks that we are properly connected to the database


@app.get("/notes/", response_model=List[Note])
async def read_notes(db: Database = Depends(get_db)):
    query = notes.select()
    return await db.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn, db: Database = Depends(get_db)):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await db.execute(query)
    return {**note.dict(), "id": last_record_id}
