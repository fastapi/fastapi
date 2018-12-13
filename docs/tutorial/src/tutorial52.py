from fastapi import Body, FastAPI, Path, Query, File
from pydantic import BaseModel
from pydantic.types import EmailStr
from typing import Set, List

app = FastAPI()


@app.post("/files/")
async def create_file(*, file: bytes = File(...)):
    return {"file_size": len(file)}
