import aiohttp
import asyncio
import math
import uvicorn

from fastapi import FastAPI, Query, Request, Response
from http import HTTPStatus
from typing import Annotated

app = FastAPI()

@app.get('/')
async def get(
        x: Annotated[float | None, Query(gt=0,                description='x')] = 1,
        y: Annotated[float | None, Query(allow_inf_nan=False, description='y')] = 0) -> str:

    assert x > 0
    assert not math.isnan(y) and not math.isinf(y)

    return 'OK'


async def main():

    config = uvicorn.Config(app, host='127.0.0.1', port=8001)
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())
    
    await asyncio.sleep(.1)

    async with aiohttp.ClientSession() as session:

        async with session.get('http://127.0.0.1:8001/?x=-1') as response:

            assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    
        async with session.get('http://127.0.0.1:8001/?y=inf') as response:

            assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    
    await server.shutdown()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())