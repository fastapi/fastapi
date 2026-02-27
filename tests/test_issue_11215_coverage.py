from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient
from starlette.background import BackgroundTasks as StarletteBackgroundTasks
from starlette.responses import Response

app = FastAPI()


@app.get("/")
def endpoint(tasks: BackgroundTasks):
    tasks.add_task(lambda: print("Dependency task"))

    response_tasks = StarletteBackgroundTasks()
    response_tasks.add_task(lambda: print("Response task"))

    return Response(
        content="Custom response",
        background=response_tasks,
    )


client = TestClient(app)


def test_issue_11215_response_background_tasks_collection(capsys):
    client.get("/")
    captured = capsys.readouterr()
    assert "Dependency task" in captured.out
    assert "Response task" in captured.out
