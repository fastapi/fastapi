from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI(form_limits={"max_fields": 5})


@app.post("/notes")
async def create_note(text: Annotated[str, Form()]):
    return {"size": len(text)}


@app.post("/documents", form_limits={"max_part_size": 2 * 1024 * 1024})
async def create_document(text: Annotated[str, Form()]):
    return {"size": len(text)}
