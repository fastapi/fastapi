import shutil
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload-product-images/")
async def upload_product_images(
    files: List[UploadFile] = File(description="Product images"),
):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    max_size = 5 * 1024 * 1024  # 5MB

    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Too many files")

    saved = []

    for file in files:
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}",
            )

        contents = await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=400, detail=f"File too large: {file.filename}"
            )

        file_ext = Path(file.filename).suffix
        unique_name = f"{uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_name

        await file.seek(0)
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved.append(
            {
                "filename": file.filename,
                "saved_as": unique_name,
                "size": len(contents),
            }
        )

    return {"uploaded": len(saved), "files": saved}
