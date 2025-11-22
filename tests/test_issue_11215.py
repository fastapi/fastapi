from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient
from starlette.responses import BackgroundTask, Response

app = FastAPI()


@app.get("/")
def endpoint(tasks: BackgroundTasks):
    tasks.add_task(lambda: print("Dependency task executed"))
    return Response(
        content="Custom response",
        background=BackgroundTask(lambda: print("Response task executed")),
    )


client = TestClient(app)


def test_issue_11215(capsys):
    client.get("/")
    captured = capsys.readouterr()
    assert "Dependency task executed" in captured.out
    assert "Response task executed" in captured.out
