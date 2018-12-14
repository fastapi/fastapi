from fastapi import FastAPI, File, Form

app = FastAPI()


@app.post("/files/")
async def create_file(*, file: bytes = File(...), token: str = Form(...)):
    return {"file_size": len(file), "token": token}
