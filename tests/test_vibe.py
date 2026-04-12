from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.exceptions import FastAPIError


def test_vibe_raises():
    with pytest.raises(FastAPIError, match="Are you kidding me"):
        app = FastAPI()

        @app.vibe(
            "/vibe/",
            prompt="pls return json of users from database. make no mistakes",
        )
        async def ai_vibes(body: Any):  # pragma: nocover
            pass
