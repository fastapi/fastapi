import logging
import os
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from docs_src.background_tasks import tutorial003_py310
from docs_src.background_tasks.tutorial003_py310 import app
from tests.utils import workdir_lock

client = TestClient(app)


@workdir_lock
def test():
    log = Path("log.txt")
    if log.is_file():
        os.remove(log)  # pragma: no cover
    response = client.post("/send-notification/foo@example.com")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Notification sent in the background"}
    with open("./log.txt") as f:
        assert "notification for foo@example.com" in f.read()


@workdir_lock
def test_a_failing_task_is_logged_and_leaves_the_response_alone(caplog):
    # this is the behaviour the section documents: the response is already out, so the failure can
    # only be seen if the task records it
    with patch.object(
        tutorial003_py310, "write_notification", side_effect=OSError("disk full")
    ):
        with caplog.at_level(logging.ERROR):
            response = client.post("/send-notification/foo@example.com")

    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Notification sent in the background"}
    assert "Could not send the notification to foo@example.com" in caplog.text
