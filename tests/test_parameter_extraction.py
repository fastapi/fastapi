from collections.abc import Iterator
from io import BytesIO
from typing import Annotated, Any, Literal

import pytest
from fastapi import FastAPI, File, Form, Header, Query, UploadFile, WebSocket
from fastapi.dependencies.utils import (
    get_dependant,
    request_body_to_args,
    request_params_to_args,
)
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, model_validator
from starlette.datastructures import FormData, Headers, MultiDict, QueryParams
from starlette.datastructures import UploadFile as StarletteUploadFile


class CountingList(list[Any]):
    visited = 0

    def __iter__(self) -> Iterator[Any]:
        for item in super().__iter__():
            self.visited += 1
            yield item


@pytest.mark.parametrize("location", ["query", "header"])
@pytest.mark.parametrize("extra", ["ignore", "allow", "forbid"])
@pytest.mark.parametrize("repeated", [False, True])
@pytest.mark.parametrize("count", [64, 128])
def test_parameter_model_extraction_has_linear_scan_cost(
    location: Literal["query", "header"],
    extra: Literal["ignore", "allow", "forbid"],
    repeated: bool,
    count: int,
):
    class Model(BaseModel):
        model_config = ConfigDict(extra=extra)
        value: str = "default"

    param = Query if location == "query" else Header

    def endpoint(data: Annotated[Model, param()]):
        return data

    dependant = get_dependant(path="/", call=endpoint)
    fields = getattr(dependant, f"{location}_params")
    items = [("unused" if repeated else f"unused-{i}", str(i)) for i in range(count)]
    if location == "header":
        received = Headers(raw=[(k.encode(), v.encode()) for k, v in items])
    else:
        received = MultiDict(items)
    backing_items = CountingList(received._list)
    received._list = backing_items

    values, errors = request_params_to_args(fields, received)

    # Count traversed entries, not elapsed time, to detect quadratic work reliably.
    assert backing_items.visited <= 10 * count
    expected_extras: dict[str, Any] = (
        {"unused": [str(i) for i in range(count)]} if repeated else dict(items)
    )
    if extra == "forbid":
        assert values == {}
        assert [(error["type"], error["loc"], error["input"]) for error in errors] == [
            ("extra_forbidden", (location, key), value)
            for key, value in expected_extras.items()
        ]
    else:
        assert errors == []
        assert endpoint(**values).model_dump() == {
            "value": "default",
            **(expected_extras if extra == "allow" else {}),
        }


@pytest.mark.anyio
@pytest.mark.parametrize("kind", ["model", "scalar", "file"])
@pytest.mark.parametrize("count", [64, 128])
async def test_form_extraction_has_linear_scan_cost(
    kind: Literal["model", "scalar", "file"], count: int
):
    class Model(BaseModel):
        value: str = "default"

    def model_endpoint(data: Annotated[Model, Form()]):
        return data

    def scalar_endpoint(value: Annotated[str, Form()] = "default"):
        return value

    def file_endpoint(upload: Annotated[UploadFile, File()]):
        return upload

    endpoint = {
        "model": model_endpoint,
        "scalar": scalar_endpoint,
        "file": file_endpoint,
    }[kind]
    dependant = get_dependant(path="/", call=endpoint)
    with BytesIO(b"contents") as contents:
        upload = UploadFile(contents, filename="example.txt")
        received = FormData(
            [(f"unused-{i}", str(i)) for i in range(count)]
            + ([("upload", upload)] if kind == "file" else [])
        )
        backing_items = CountingList(received._list)
        received._list = backing_items

        values, errors = await request_body_to_args(
            body_fields=dependant.body_params,
            received_body=received,
            embed_body_fields=False,
        )

        assert errors == []
        assert backing_items.visited <= 10 * len(received)
        if kind == "model":
            assert endpoint(**values).model_dump() == {"value": "default"}
        elif kind == "scalar":
            assert values == {"value": "default"}
            assert endpoint(**values) == "default"
        else:
            assert endpoint(**values) is upload
            assert contents.tell() == 0


@pytest.mark.anyio
@pytest.mark.parametrize("location", ["query", "header", "form"])
async def test_model_before_validator_receives_ignored_extras(
    location: Literal["query", "header", "form"],
):
    inputs: list[dict[str, Any]] = []

    class Model(BaseModel):
        model_config = ConfigDict(extra="ignore")
        tags: list[str]

        @model_validator(mode="before")
        @classmethod
        def inspect_input(cls, value: Any) -> Any:
            inputs.append(value.copy())
            return value

    param = {"query": Query, "header": Header, "form": Form}[location]

    def endpoint(data: Annotated[Model, param()]):
        return data

    items = [
        ("tags", "one"),
        ("extra", "first"),
        ("empty", ""),
        ("tags", "two"),
        ("extra", "second"),
    ]
    dependant = get_dependant(path="/", call=endpoint)
    if location == "form":
        values, errors = await request_body_to_args(
            body_fields=dependant.body_params,
            received_body=FormData([*items]),
            embed_body_fields=False,
        )
    else:
        received = (
            Headers(raw=[(key.encode(), value.encode()) for key, value in items])
            if location == "header"
            else QueryParams(items)
        )
        values, errors = request_params_to_args(
            getattr(dependant, f"{location}_params"), received
        )

    assert errors == []
    # Extras reach before-validators even when field validation ignores them.
    assert inputs == [
        {"tags": ["one", "two"], "extra": ["first", "second"], "empty": ""}
    ]
    assert endpoint(**values).model_dump() == {"tags": ["one", "two"]}


@pytest.mark.parametrize("location", ["query", "header"])
def test_parameter_model_extras_reflect_mutation(
    location: Literal["query", "header"],
):
    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        value: str = "default"

    param = Query if location == "query" else Header

    def endpoint(data: Annotated[Model, param()]):
        return data

    dependant = get_dependant(path="/", call=endpoint)
    fields = getattr(dependant, f"{location}_params")
    if location == "header":
        received = Headers(
            raw=[(b"extra", b"first"), (b"extra", b"second")]
        ).mutablecopy()
    else:
        received = MultiDict([("extra", "first"), ("extra", "second")])

    before, errors = request_params_to_args(fields, received)
    assert errors == []
    received.update({"extra": "changed"})
    after, errors = request_params_to_args(fields, received)
    assert errors == []
    assert endpoint(**before).model_extra == {"extra": ["first", "second"]}
    assert endpoint(**after).model_extra == {"extra": "changed"}


@pytest.mark.parametrize("location", ["query", "header"])
def test_websocket_parameter_models_preserve_repeated_extras(
    location: Literal["query", "header"],
):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        value: str

    param = Query if location == "query" else Header

    @app.websocket("/ws")
    async def endpoint(websocket: WebSocket, data: Annotated[Model, param()]):
        assert data.model_extra is not None
        await websocket.accept()
        await websocket.send_json(
            {
                "value": data.value,
                "extra": data.model_extra["extra"],
                "single": data.model_extra["single"],
            }
        )
        await websocket.close()

    items = [
        ("value", "known"),
        ("extra", "first"),
        ("single", "one"),
        ("extra", "second"),
    ]
    client = TestClient(app)
    if location == "query":
        connection = client.websocket_connect("/ws", params=items)
    else:
        # Preserve duplicate lines using the TestClient's HTTPX backend.
        client.headers = [(key.upper(), value) for key, value in items]
        connection = client.websocket_connect("/ws")
    with connection as websocket:
        assert websocket.receive_json() == {
            "value": "known",
            "extra": ["first", "second"],
            "single": "one",
        }


@pytest.mark.anyio
@pytest.mark.parametrize("count", [64, 128])
async def test_form_union_normalization_has_linear_scan_cost(
    monkeypatch: pytest.MonkeyPatch, count: int
):
    backing_lists: list[CountingList] = []
    original_init = FormData.__init__

    def track_items(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        backing = CountingList(self._list)
        self._list = backing
        backing_lists.append(backing)

    monkeypatch.setattr(FormData, "__init__", track_items)

    class First(BaseModel):
        kind: Literal["first"]

    class Second(BaseModel):
        kind: Literal["second"]
        tags: list[str]

    def endpoint(data: Annotated[First | Second, Form()]):
        return data

    dependant = get_dependant(path="/", call=endpoint)
    received = FormData(
        [("kind", "second"), ("tags", "one"), ("tags", "two")]
        + [(f"unused-{i}", str(i)) for i in range(count)]
    )
    values, errors = await request_body_to_args(
        body_fields=dependant.body_params,
        received_body=received,
        embed_body_fields=False,
    )

    assert errors == []
    assert endpoint(**values).model_dump() == {
        "kind": "second",
        "tags": ["one", "two"],
    }
    # Include the FormData objects created while normalizing union branches.
    assert sum(backing.visited for backing in backing_lists) <= 10 * (count + 3)


def test_multipart_extras_preserve_files_text_and_cleanup():
    app = FastAPI()
    uploads: list[StarletteUploadFile] = []

    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        value: str

    @app.post("/")
    def endpoint(data: Annotated[Model, Form()]):
        assert data.model_extra is not None
        mixed = data.model_extra["mixed"]
        single = data.model_extra["single"]
        uploads.extend([mixed[0], mixed[2], single])
        assert all(isinstance(upload, StarletteUploadFile) for upload in uploads)
        assert all(upload.file.tell() == 0 for upload in uploads)
        assert all(not upload.file.closed for upload in uploads)
        return {
            "value": data.value,
            "mixed": [mixed[0].filename, mixed[1], mixed[2].filename],
            "single": single.filename,
            "empty": data.model_extra["empty"],
        }

    response = TestClient(app).post(
        "/",
        files=[
            ("value", (None, "known")),
            ("mixed", ("first.txt", b"first")),
            ("empty", (None, "")),
            ("mixed", (None, "text")),
            ("single", ("single.txt", b"single")),
            ("mixed", ("second.txt", b"second")),
        ],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {
        "value": "known",
        "mixed": ["first.txt", "text", "second.txt"],
        "single": "single.txt",
        "empty": "",
    }
    assert len(uploads) == 3
    assert all(upload.file.closed for upload in uploads)
