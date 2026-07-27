from typing import Any

import orjson
from fastapi import FastAPI, Response

app = FastAPI()


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}
