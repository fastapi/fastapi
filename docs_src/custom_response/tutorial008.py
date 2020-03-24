from fastapi import FastAPI
from fastapi.responses import StreamingResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()


@app.get("/")
def main():
    file_like = open(some_file_path, mode="rb")
    return StreamingResponse(file_like, media_type="video/mp4")
