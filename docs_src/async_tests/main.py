from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize a shared state when the app starts
    app.state.some_state = "some_state_open"
    yield
    # Cleanup the shared state when the app shuts down
    app.state.some_state = "some_state_close"


async def get_some_state(request: Request):
    return request.app.state.some_state


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(some_state=Depends(get_some_state)):
    return {"message": some_state}
