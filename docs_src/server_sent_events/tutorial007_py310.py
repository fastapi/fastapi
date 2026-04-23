from collections.abc import AsyncIterable

from fastapi import FastAPI, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

app = FastAPI()

# Track disconnects for testing
disconnect_events: list[str] = []


async def on_disconnect(request: Request) -> None:
    """Callback invoked when client disconnects."""
    disconnect_events.append("client_disconnected")


# Custom EventSourceResponse subclass with disconnect callback
class DisconnectCallbackEventSourceResponse(EventSourceResponse):
    """EventSourceResponse with an on_disconnect callback."""

    on_disconnect = on_disconnect


class Item(BaseModel):
    name: str
    price: float


items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]


@app.get("/items/stream", response_class=DisconnectCallbackEventSourceResponse)
async def stream_items_with_disconnect() -> AsyncIterable[ServerSentEvent]:
    """Stream items with disconnect callback."""
    for i, item in enumerate(items):
        yield ServerSentEvent(data=item, event="item_update", id=str(i + 1))


@app.get(
    "/items/stream-infinite",
    response_class=DisconnectCallbackEventSourceResponse,
)
async def stream_items_infinite() -> AsyncIterable[ServerSentEvent]:
    """Stream items infinitely - disconnect callback should fire on client disconnect."""
    i = 0
    while True:
        yield ServerSentEvent(data={"count": i}, event="tick", id=str(i))
        i += 1
