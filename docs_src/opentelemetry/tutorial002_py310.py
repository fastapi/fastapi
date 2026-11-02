from fastapi import FastAPI
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

app = FastAPI(telemetry={"tracer_provider": tracer_provider})


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
