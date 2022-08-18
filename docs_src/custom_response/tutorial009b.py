from fastapi import FastAPI
from fastapi.responses import FileResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()


@app.get("/", response_class=FileResponse)
async def main():
    return some_file_path
