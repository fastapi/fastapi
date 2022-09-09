from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes | None = File(default=None)):
    return {"file_size": len(file)} if file else {"message": "No file sent"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    return (
        {"filename": file.filename}
        if file
        else {"message": "No upload file sent"}
    )
