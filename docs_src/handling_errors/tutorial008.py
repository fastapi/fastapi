from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

MAX_FILE_SIZE_MB = 5
ALLOWED_TYPES = {"application/pdf", "image/jpeg"}

app = FastAPI()


class FileTooLargeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=413, detail="The uploaded file is too large.")


class UnsupportedFileTypeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=415, detail="Unsupported file type")


@app.exception_handler((FileTooLargeError, UnsupportedFileTypeError))
async def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "hint": "Need help? Contact support@example.com"},
    )


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise UnsupportedFileTypeError()

    # Validate file size (read contents to check size in memory)
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise FileTooLargeError()

    return {"filename": file.filename, "message": "File uploaded successfully!"}
