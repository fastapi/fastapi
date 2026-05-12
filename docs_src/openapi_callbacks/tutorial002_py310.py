import httpx
from fastapi import BackgroundTasks, FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class PassageProcessingRequest(BaseModel):
    passage_topic: str
    callback_url: str


@app.post("/callback")
async def callback(request: Request):
    """
    Receives the processing result from the server.

    In a real-world application, this endpoint would typically belong
    to a different service or client application.

    The server sends a POST request to this URL once the background
    processing is completed.
    """

    data = await request.json()

    print(data)

    return {"received": True}


async def send_processing_result(callback_url: str, generated_passage: str):
    """
    Sends the processed passage result to the client's callback URL.
    """

    async with httpx.AsyncClient() as client:
        await client.post(
            callback_url,
            json={"processed_passage": generated_passage, "status": "completed"},
        )


@app.post("/process-passage")
async def process_passage(
    data: PassageProcessingRequest, background_tasks: BackgroundTasks
):
    """
    Receives a passage processing request from the client.

    Passage generation may take a long time to complete.
    Instead of keeping the client waiting, the server immediately
    returns a response and processes the task in the background.

    Once processing is completed, the server sends the result
    to the callback URL.
    """

    background_tasks.add_task(
        send_processing_result, data.callback_url, data.passage_topic
    )

    return {"message": "Passage processing started"}
