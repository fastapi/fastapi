from fastapi import FastAPI

app = FastAPI()


@app.get("/files/{file_path:path}")
async def read_user_me(file_path: str):
    return {"file_path": file_path}
