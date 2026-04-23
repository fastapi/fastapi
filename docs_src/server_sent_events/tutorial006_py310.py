from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]


# Custom EventSourceResponse subclass with default retry configuration
class RetryEventSourceResponse(EventSourceResponse):
    """EventSourceResponse with a default retry time of 3000ms."""

    default_retry = 3000


class OverrideRetryEventSourceResponse(EventSourceResponse):
    """EventSourceResponse with a default retry time of 3000ms (can be overridden per-event)."""

    default_retry = 3000


@app.get("/items/stream", response_class=RetryEventSourceResponse)
async def stream_items_with_default_retry() -> AsyncIterable[ServerSentEvent]:
    """Stream items with a default retry of 3000ms."""
    for i, item in enumerate(items):
        yield ServerSentEvent(data=item, event="item_update", id=str(i + 1))


@app.get(
    "/items/stream-override",
    response_class=OverrideRetryEventSourceResponse,
)
async def stream_items_override_retry() -> AsyncIterable[ServerSentEvent]:
    """Stream items where individual events can override the default retry."""
    for i, item in enumerate(items):
        # Override default retry for this specific event
        yield ServerSentEvent(
            data=item, event="item_update", id=str(i + 1), retry=10000
        )


@app.get("/items/stream-plain", response_class=EventSourceResponse)
async def stream_items_plain() -> AsyncIterable[Item]:
    """Stream items as plain objects (automatically formatted as SSE)."""
    for item in items:
        yield item
