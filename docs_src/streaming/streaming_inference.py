"""
Streaming inference example using StreamingResponse.

This pattern is useful for long-running workloads such as machine learning
or large language model inference, where returning partial results improves
latency and user experience.
"""

import time
from collections.abc import Generator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


def fake_model_inference(prompt: str) -> Generator[str, None, None]:
    """
    Simulates token-by-token inference.

    In a real application, this could wrap a machine learning model that
    yields partial outputs as they are generated.
    """
    try:
        for i in range(10):
            # Simulate computation time (e.g. model forward pass)
            time.sleep(0.2)
            yield f"token_{i} for prompt='{prompt}'\n"
    except GeneratorExit:
        # This is triggered when the client disconnects early.
        # Cleanup logic for model inference can be placed here.
        print("Client disconnected, stopping inference")


@app.get("/stream")
def stream(prompt: str) -> StreamingResponse:
    """
    Stream inference results incrementally to the client.

    This endpoint returns partial results as they become available instead
    of waiting for the full inference to complete, making the user experience better.
    """
    return StreamingResponse(
        fake_model_inference(prompt),
        media_type="text/plain",
    )
