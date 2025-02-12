import asyncio
import builtins

from fastapi.testclient import TestClient

from docs_src.background_tasks import tutorial002_an


# No additional imports are needed.
# No additional imports are required beyond those already present in the test file.
def test_send_notification_with_query(monkeypatch):
    """
    Test sending a notification with a query parameter.
    This test monkeypatches the write_log function to capture log messages
    instead of writing to a file. It verifies that both the dependency and the endpoint
    add the correct background tasks that call write_log with the expected messages.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/test@example.com?q=somequery")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: somequery\n", "message to test@example.com\n"]
    assert log_messages == expected


def test_send_notification_without_query(monkeypatch):
    """
    Test sending a notification without a query parameter.
    This test monkeypatches the write_log function to capture log messages.
    It verifies that when no query parameter is provided:
    - The dependency does not add a log message.
    - Only the endpoint adds the expected log message.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/test@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["message to test@example.com\n"]
    assert log_messages == expected


def test_get_query_direct_with_query():
    """
    Test the get_query function directly by using a fake BackgroundTasks object.
    This verifies that when a query value is provided:
    - The function returns the query value.
    - A background task is added with the correct message using the write_log function.
    """

    class FakeBackgroundTasks:
        def __init__(self):
            self.tasks = []

        def add_task(self, func, *args, **kwargs):
            self.tasks.append((func, args, kwargs))

    fake_bg = FakeBackgroundTasks()
    query = "directTestQuery"
    result = tutorial002_an.get_query(fake_bg, query)
    assert result == query
    assert len(fake_bg.tasks) == 1
    func, args, kwargs = fake_bg.tasks[0]
    expected_message = f"found query: {query}\n"
    assert func == tutorial002_an.write_log
    assert args[0] == expected_message


def test_get_query_direct_without_query():
    """
    Test the get_query function directly by using a fake BackgroundTasks object when no query is provided.
    This verifies that when the query is None:
    - The function returns None.
    - No background task is added.
    """

    class FakeBackgroundTasks:
        def __init__(self):
            self.tasks = []

        def add_task(self, func, *args, **kwargs):
            self.tasks.append((func, args, kwargs))

    fake_bg = FakeBackgroundTasks()
    result = tutorial002_an.get_query(fake_bg, None)
    assert result is None
    assert len(fake_bg.tasks) == 0


def test_send_notification_with_empty_query(monkeypatch):
    """
    Test sending a notification with an empty query parameter.
    This verifies that when an empty query string is provided:
    - The dependency treats the empty query as valid and schedules a background task.
    - The endpoint also schedules its own background task.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/test@example.com?q=")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: \n", "message to test@example.com\n"]
    assert log_messages == expected


def test_invalid_method_returns_405():
    """
    Test that sending an invalid HTTP method (GET) to the POST endpoint returns a 405 error.
    """
    client = TestClient(tutorial002_an.app)
    response = client.get("/send-notification/test@example.com")
    assert response.status_code == 405


def test_write_log_writes_to_file(monkeypatch):
    """
    Test that the write_log function writes the provided message to a file in append mode.
    This is done by monkeypatching the built-in open function to capture file writes.
    """
    written_data = []

    class FakeFile:
        def write(self, msg):
            written_data.append(msg)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def fake_open(file, mode):
        assert file == "log.txt"
        assert mode == "a"
        return FakeFile()

    monkeypatch.setattr(builtins, "open", fake_open)
    tutorial002_an.write_log("file test message\n")
    assert written_data == ["file test message\n"]


def test_background_tasks_execution_order_manual(monkeypatch):
    """
    Test that background tasks are scheduled and executed in the expected order.
    This test manually creates a fake BackgroundTasks object, schedules tasks via the
    dependency and endpoint, and then executes them to verify the correct ordering.
    """
    log_order = []

    def fake_write_log(message: str):
        log_order.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)

    class FakeBackgroundTasks:
        def __init__(self):
            self.tasks = []

        def add_task(self, func, *args, **kwargs):
            self.tasks.append((func, args, kwargs))

    fake_bg = FakeBackgroundTasks()

    result_query = tutorial002_an.get_query(fake_bg, "orderTest")
    assert result_query == "orderTest"

    response = asyncio.run(
        tutorial002_an.send_notification("order@example.com", fake_bg, result_query)
    )
    assert response == {"message": "Message sent"}

    assert len(fake_bg.tasks) == 2
    expected_task_args = [
        ("found query: orderTest\n",),
        ("message to order@example.com\n",),
    ]

    for i, task in enumerate(fake_bg.tasks):
        func, args, kwargs = task
        assert args == expected_task_args[i]
        func(*args, **kwargs)

    assert log_order == ["found query: orderTest\n", "message to order@example.com\n"]


def test_send_notification_multiple_query_params(monkeypatch):
    """
    Test sending a notification with multiple 'q' query parameters.
    This verifies that when multiple values are provided for the query parameter,
    FastAPI takes the last one. The test monkeypatches write_log to capture the log messages,
    and then asserts that the dependency and the endpoint add the correct messages.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/test@example.com?q=first&q=second")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: second\n", "message to test@example.com\n"]
    assert log_messages == expected


def test_send_notification_background_task_exception(monkeypatch):
    """
    Test that if the background task (write_log) raises an exception,
    the endpoint still returns a 200 status with the expected message,
    by configuring the TestClient to not raise server exceptions.
    """

    def failing_write_log(message: str):
        raise Exception("Simulated failure in background task")

    monkeypatch.setattr(tutorial002_an, "write_log", failing_write_log)
    client = TestClient(tutorial002_an.app, raise_server_exceptions=False)
    response = client.post("/send-notification/test@example.com?q=failure")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}


def test_openapi_schema_contains_query_parameter():
    """
    Test that the OpenAPI schema for the send_notification endpoint includes
    the query parameter 'q' from the dependency.
    """
    openapi_schema = tutorial002_an.app.openapi()
    post_schema = openapi_schema["paths"]["/send-notification/{email}"]["post"]
    parameters = post_schema.get("parameters", [])
    q_parameters = [
        param
        for param in parameters
        if param.get("name") == "q" and param.get("in") == "query"
    ]
    assert (
        len(q_parameters) == 1
    ), "Expected one query parameter named 'q' in the OpenAPI schema"


def test_dependency_exception(monkeypatch):
    """
    Test that if the dependency (get_query) raises an exception,
    the overall endpoint returns a 500 error.
    """
    original_get_query = tutorial002_an.get_query

    def failing_get_query(
        background_tasks: tutorial002_an.BackgroundTasks, q: str = None
    ):
        raise Exception("Simulated dependency failure")

    tutorial002_an.app.dependency_overrides[tutorial002_an.get_query] = (
        failing_get_query
    )
    client = TestClient(tutorial002_an.app, raise_server_exceptions=False)
    response = client.post("/send-notification/test@example.com?q=test")
    assert response.status_code == 500
    tutorial002_an.app.dependency_overrides.pop(tutorial002_an.get_query, None)


def test_send_notification_with_whitespace_query(monkeypatch):
    """
    Test sending a notification with a whitespace query parameter.
    This verifies that when a query containing only whitespace is provided,
    the dependency adds a background task with the exact whitespace in the message,
    and the endpoint also adds its own background task.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/test@example.com?q=   ")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query:    \n", "message to test@example.com\n"]
    assert log_messages == expected


def test_openapi_schema_query_optional():
    """
    Test that the OpenAPI schema for the send_notification endpoint marks the query parameter 'q' as optional.
    This ensures that clients are not forced to include the query parameter.
    """
    openapi_schema = tutorial002_an.app.openapi()
    post_schema = openapi_schema["paths"]["/send-notification/{email}"]["post"]
    parameters = post_schema.get("parameters", [])
    q_parameters = [
        param
        for param in parameters
        if param.get("name") == "q" and param.get("in") == "query"
    ]
    assert (
        len(q_parameters) == 1
    ), "Expected one query parameter named 'q' in the OpenAPI schema"
    q_param = q_parameters[0]
    assert q_param.get("required") is False, "Query parameter 'q' should be optional"


def test_get_query_with_non_string_value():
    """
    Test calling get_query with a non-string value (an integer).
    This verifies that even though the type hint expects a str or None,
    get_query will convert a non-string (here, int) to its string representation,
    schedule a background task, and return the original value.
    """

    class FakeBackgroundTasks:
        def __init__(self):
            self.tasks = []

        def add_task(self, func, *args, **kwargs):
            self.tasks.append((func, args, kwargs))

    fake_bg = FakeBackgroundTasks()
    non_str_query = 42
    result = tutorial002_an.get_query(fake_bg, non_str_query)
    assert result == non_str_query
    assert len(fake_bg.tasks) == 1
    func, args, kwargs = fake_bg.tasks[0]
    expected_message = f"found query: {non_str_query}\n"
    assert func == tutorial002_an.write_log
    assert args[0] == expected_message


def test_openapi_schema_contains_email_parameter():
    """
    Test that the OpenAPI schema for the send_notification endpoint includes
    the path parameter 'email' and that it is required and of type string.
    This ensures that the API documentation correctly reflects the need for an email value.
    """
    openapi_schema = tutorial002_an.app.openapi()
    post_schema = openapi_schema["paths"]["/send-notification/{email}"]["post"]
    parameters = post_schema.get("parameters", [])
    email_parameters = [
        param
        for param in parameters
        if param.get("name") == "email" and param.get("in") == "path"
    ]
    assert (
        len(email_parameters) == 1
    ), "Expected one path parameter named 'email' in the OpenAPI schema"
    email_param = email_parameters[0]
    assert (
        email_param.get("required") is True
    ), "Path parameter 'email' should be required"
    schema = email_param.get("schema", {})
    assert (
        schema.get("type") == "string"
    ), "Path parameter 'email' should be of type string"


def test_send_notification_with_invalid_email_format(monkeypatch):
    """
    Test that the send_notification endpoint accepts an invalid email format.
    The test verifies that even if the email parameter is not a valid email,
    both the dependency and the endpoint schedule their background tasks correctly.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    # Send a POST request to a path with an invalid email format and a query parameter
    response = client.post("/send-notification/invalid?q=invalidQuery")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: invalidQuery\n", "message to invalid\n"]
    assert log_messages == expected


def test_send_notification_with_plus_in_email(monkeypatch):
    """
    Test sending a notification where the email contains a '+' character (e.g., user+alias@example.com).
    This verifies that the endpoint accepts special characters in the email and that both the dependency and
    the endpoint schedule background tasks with the correct log messages.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/user+alias@example.com?q=plus")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: plus\n", "message to user+alias@example.com\n"]
    assert log_messages == expected


def test_send_notification_with_spaces_in_email(monkeypatch):
    """
    Test sending a notification where the path parameter email includes leading and trailing spaces.
    Verifies that the endpoint accepts the encoded email, decodes it correctly, and that both the dependency
    and endpoint schedule background tasks with the exact email value.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    # Define an email with leading and trailing spaces.
    email = " test@example.com "
    # URL-encode the email manually (spaces become '%20').
    encoded_email = email.replace(" ", "%20")
    response = client.post(f"/send-notification/{encoded_email}?q=spaceTest")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: spaceTest\n", f"message to {email}\n"]
    assert log_messages == expected


def test_send_notification_with_unicode_query(monkeypatch):
    """
    Test sending a notification with a Unicode query parameter.
    This verifies that the endpoint correctly handles non-ASCII (Unicode) characters
    in the query, scheduling background tasks with the precise log messages.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    # Unicode query parameter "こんにちは" (Hello in Japanese)
    response = client.post("/send-notification/user@example.com?q=こんにちは")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: こんにちは\n", "message to user@example.com\n"]
    assert log_messages == expected


def test_send_notification_with_numeric_email(monkeypatch):
    """
    Test sending a notification where the email path parameter is numeric (e.g., '123').
    This verifies that the endpoint correctly handles numeric email inputs by treating
    them as strings and scheduling the background task to log the correct message.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    response = client.post("/send-notification/123")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["message to 123\n"]
    assert log_messages == expected


def test_send_notification_with_special_whitespace(monkeypatch):
    """
    Test sending a notification with a query parameter containing tabs and newlines.
    This verifies that the dependency and endpoint preserve special whitespace characters in the query,
    and schedule background tasks that log exactly the expected messages.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)

    # Define a query containing a tab and a newline.
    special_query = "line1\tline2\nline3"
    response = client.post(
        "/send-notification/special@example.com", params={"q": special_query}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}

    expected = [f"found query: {special_query}\n", "message to special@example.com\n"]
    assert log_messages == expected


def test_send_notification_extra_query_parameters(monkeypatch):
    """
    Test sending a notification with extra query parameters.
    This verifies that additional, unexpected query parameters (like 'foo') are ignored by the endpoint,
    and only the expected 'q' parameter is processed.
    """
    log_messages = []

    def fake_write_log(message: str):
        log_messages.append(message)

    monkeypatch.setattr(tutorial002_an, "write_log", fake_write_log)
    client = TestClient(tutorial002_an.app)
    # Send the request with both 'q' and an extra 'foo' parameter
    response = client.post("/send-notification/extra@example.com?q=extraTest&foo=bar")
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}
    expected = ["found query: extraTest\n", "message to extra@example.com\n"]
    assert log_messages == expected
