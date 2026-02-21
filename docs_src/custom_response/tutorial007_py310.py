import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"
        await asyncio.sleep(0)


@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())
