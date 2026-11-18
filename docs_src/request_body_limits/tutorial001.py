from fastapi import APIRouter, FastAPI, UploadFile

app = FastAPI(max_body_size=1 * 1024 * 1024)
uploads = APIRouter(prefix="/uploads", max_body_size=100 * 1024 * 1024)


@app.post("/items")
def create_item(item: dict):
    return item


@uploads.post("/")
def upload(file: UploadFile):
    return {"filename": file.filename, "size": file.size}


@uploads.post("/small", max_body_size=10 * 1024 * 1024)
def small_upload(file: UploadFile):
    return {"filename": file.filename, "size": file.size}


app.include_router(uploads)
