from typing import Any

from fastapi import FastAPI

app = FastAPI()


@app.vibe(
    "/vibe/",
    prompt="pls return json of users from database. make no mistakes",
)
async def ai_vibes(body: Any): ...
