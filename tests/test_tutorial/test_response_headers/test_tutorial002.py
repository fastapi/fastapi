from fastapi.testclient import TestClient
from docs_src.response_headers.tutorial002 import app
from docs_src.background_tasks.tutorial002 import app as background_app
from fastapi import BackgroundTasks
from docs_src.background_tasks.tutorial002 import get_query, write_log

client = TestClient(app)
def test_path_operation():
    response = client.get("/headers-and-object/")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World"}
    assert response.headers["X-Cat-Dog"] == "alone in the world"
def test_send_notification_with_query():
    """
    Test the /send-notification/{email} endpoint with a provided query parameter.
    This verifies that when a query string is given, both the dependency and the endpoint add
    background tasks and the endpoint returns the expected success message.
    """
    client = TestClient(background_app)
    response = client.post("/send-notification/test@example.com?q=Hello")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Message sent"}
def test_send_notification_without_query():
    """
    Test the /send-notification/{email} endpoint without providing a query parameter.
    This verifies that when no query string is given, the dependency doesn't add any extra
    background tasks, and the endpoint returns the expected success message.
    """
    client = TestClient(background_app)
    response = client.post("/send-notification/test@example.com")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Message sent"}
def test_get_query_dependency():
    """
    Test that the get_query dependency function:
      - Returns the provided query string.
      - Adds a background task when a query is provided.
      - Does not add any task when no query is provided (i.e. q is None).
    """
    # Test with a provided query string.
    bt = BackgroundTasks()
    query_result = get_query(bt, "TestQuery")
    assert query_result == "TestQuery"
    # BackgroundTasks stores tasks in the 'tasks' list.
    assert len(bt.tasks) == 1
    # Test with no query provided (None).
    bt_none = BackgroundTasks()
    query_none = get_query(bt_none, None)
    assert query_none is None
    assert len(bt_none.tasks) == 0from fastapi import BackgroundTasks
from docs_src.background_tasks.tutorial002 import get_query, write_log


def test_get_query_with_empty_string():
    """
    Test the get_query dependency when an empty string is provided as the query.
    This verifies that an empty string is returned and that a background task 
    is added with the expected log message ("found query: \n").
    """
    bt = BackgroundTasks()
    result = get_query(bt, "")
    
    # Verify that the dependency returns an empty string.
    assert result == ""
    
    # Verify that one background task has been added.
    assert len(bt.tasks) == 1
    
    # Each task is a tuple: (callable, args, kwargs).
    task_callable, task_args, task_kwargs = bt.tasks[0]
    # Check that the task is to call write_log.
    assert task_callable is write_log
    # Check that the argument is the expected log message.
    assert task_args == ("found query: \n",)
    # There should be no keyword arguments.
    assert task_kwargs == {}
from fastapi import BackgroundTasks
from docs_src.background_tasks.tutorial002 import get_query, write_log
from starlette.background import BackgroundTask


def test_get_query_with_empty_string():
    """
    Test that the get_query dependency, when provided an empty string as the query,
    returns an empty string and schedules a background task with the expected log message.
    """
    bt = BackgroundTasks()
    result = get_query(bt, "")
    
    # Verify that the dependency returns an empty string.
    assert result == ""
    
    # Verify that one background task has been added.
    assert len(bt.tasks) == 1
    
    # Retrieve the scheduled task.
    task = bt.tasks[0]
    
    # Verify that the task is a BackgroundTask instance.
    assert isinstance(task, BackgroundTask)
    
    # Verify that the task is to call write_log with the expected log message.
    assert task.func is write_log
    assert task.args == ("found query: \n",)
    assert task.kwargs == {}
from fastapi.testclient import TestClient
from fastapi import BackgroundTasks
from starlette.background import BackgroundTask
from docs_src.response_headers.tutorial002 import app  # ... existing code
from docs_src.background_tasks.tutorial002 import app as background_app
from docs_src.background_tasks.tutorial002 import get_query, write_log


def test_path_operation():
    """
    Test that the /headers-and-object/ endpoint returns the expected JSON object and headers.
    """
    response = TestClient(app).get("/headers-and-object/")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World"}
    assert response.headers["X-Cat-Dog"] == "alone in the world"


def test_send_notification_with_query():
    """
    Test the /send-notification/{email} endpoint with a provided query parameter.
    This verifies that when a query string is given, both the dependency and the endpoint add
    background tasks and the endpoint returns the expected success message.
    """
    client = TestClient(background_app)
    response = client.post("/send-notification/test@example.com?q=Hello")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Message sent"}


def test_send_notification_without_query():
    """
    Test the /send-notification/{email} endpoint without providing a query parameter.
    This verifies that when no query string is given, the dependency doesn't add any extra
    background tasks, and the endpoint returns the expected success message.
    """
    client = TestClient(background_app)
    response = client.post("/send-notification/test@example.com")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Message sent"}


def test_get_query_dependency():
    """
    Test that the get_query dependency function:
      - Returns the provided query string.
      - Adds a background task when a query is provided.
      - Does not add any task when no query is provided (i.e. q is None).
    """
    # Test with a provided query string.
    bt = BackgroundTasks()
    query_result = get_query(bt, "TestQuery")
    assert query_result == "TestQuery"
    # BackgroundTasks stores tasks as BackgroundTask instances.
    assert len(bt.tasks) == 1

    # Test with no query provided (None).
    bt_none = BackgroundTasks()
    query_none = get_query(bt_none, None)
    assert query_none is None
    assert len(bt_none.tasks) == 0


def test_get_query_with_empty_string():
    """
    Test that the get_query dependency, when provided an empty string as the query,
    returns an empty string and schedules a background task with the expected log message.
    """
    bt = BackgroundTasks()
    result = get_query(bt, "")
    
    # Verify that the dependency returns an empty string.
    assert result == ""
    
    # Verify that one background task has been added.
    assert len(bt.tasks) == 1
    
    # Retrieve the scheduled task.
    task = bt.tasks[0]
    
    # Verify that the task is a BackgroundTask instance.
    assert isinstance(task, BackgroundTask)
    
    # Verify that the task is to call write_log with the expected log message.
    assert task.func is write_log
    assert task.args == ("found query: \n",)
    assert task.kwargs == {}
