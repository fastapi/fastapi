from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()


@app.post("/upload-images/")
async def upload_images(
    files: Annotated[list[UploadFile], File(description="Multiple images")],
):
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    max_size = 5 * 1024 * 1024  # 5MB

    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Too many files")

    results = []

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

        await file.seek(0)

        results.append(
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(contents),
            }
        )

    return {"uploaded": len(results), "files": results}
