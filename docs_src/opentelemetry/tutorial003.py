from fastapi import FastAPI

app = FastAPI(telemetry={"operation_spans": False})


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
