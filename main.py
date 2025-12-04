from typing import Union

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/upload")
async def upload_file(file: UploadFile = File(max_size=500)):
    total_bytes = 0
    
    # Safest: process in chunks instead of reading whole file
    while True:
        chunk = await file.read(1024 * 1024)  # 1MB
        if not chunk:
            break
        total_bytes += len(chunk)

    return {"filename": file.filename, "size": total_bytes}


