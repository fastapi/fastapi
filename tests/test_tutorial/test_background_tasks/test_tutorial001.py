import os
from pathlib import Path

from fastapi.testclient import TestClient

from background_tasks.tutorial001 import app

client = TestClient(app)


def test():
    log = Path("log.txt")
    if log.is_file():
        os.remove(log)  # pragma: no cover
    response = client.post("/send-notification/foo@example.com")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Notification sent in the background"}
    with open("./log.txt") as f:
        assert "notification for foo@example.com: some notification" in f.read()
