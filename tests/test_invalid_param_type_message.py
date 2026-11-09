from typing import Annotated

import pytest
from fastapi import Depends, FastAPI, Query
from fastapi.exceptions import FastAPIError


class NotAModel:
    pass


def test_invalid_request_parameter_type_message() -> None:
    app = FastAPI()

    def create_item(item: NotAModel):
        return item  # pragma: no cover

    with pytest.raises(FastAPIError) as exc_info:
        app.post("/items")(create_item)

    message = str(exc_info.value)
    assert message.startswith(
        "Invalid type annotation for the request parameter 'item'! Hint: check that "
    )
    assert "is a valid Pydantic field type" in message
    assert "response" not in message


def test_invalid_query_parameter_type_in_dependency_message() -> None:
    app = FastAPI()

    def get_filters(filters: Annotated[NotAModel, Query()]):
        return filters  # pragma: no cover

    def search(filters=Depends(get_filters)):
        return filters  # pragma: no cover

    with pytest.raises(
        FastAPIError,
        match="Invalid type annotation for the request parameter 'filters'",
    ):
        app.get("/search")(search)


def test_invalid_response_model_message_is_unchanged() -> None:
    app = FastAPI()

    def read_item() -> NotAModel:
        return NotAModel()  # pragma: no cover

    with pytest.raises(FastAPIError) as exc_info:
        app.get("/item")(read_item)

    message = str(exc_info.value)
    assert message.startswith("Invalid args for response field! Hint: check that ")
    assert "response_model=None" in message
