from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/preferences/")
async def update_preferences(subscribe: Annotated[bool, Form()] = False):
    return {"subscribe": subscribe}
