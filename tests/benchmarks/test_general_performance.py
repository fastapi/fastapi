import json
import sys
import warnings
from collections.abc import Iterator
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

if "--codspeed" not in sys.argv:
    pytest.skip(
        "Benchmark tests are skipped by default; run with --codspeed.",
        allow_module_level=True,
    )

LARGE_ITEMS: list[dict[str, Any]] = [
    {
        "id": i,
        "name": f"item-{i}",
        "values": list(range(25)),
        "meta": {
            "active": True,
            "group": i % 10,
            "tag": f"t{i % 5}",
        },
    }
    for i in range(300)
]

LARGE_METADATA: dict[str, Any] = {
    "source": "benchmark",
    "version": 1,
    "flags": {"a": True, "b": False, "c": True},
    "notes": ["x" * 50, "y" * 50, "z" * 50],
}

LARGE_PAYLOAD: dict[str, Any] = {"items": LARGE_ITEMS, "metadata": LARGE_METADATA}


def dep_a():
    return 40


def dep_b(a: Annotated[int, Depends(dep_a)]):
    return a + 2


@pytest.fixture(
    scope="module",
    params=[
        "pydantic-v2",
        "pydantic-v1",
    ],
)
def basemodel_class(request: pytest.FixtureRequest) -> type[Any]:
    if request.param == "pydantic-v2":
        from pydantic import BaseModel

        return BaseModel
    else:
        from pydantic.v1 import BaseModel

        return BaseModel


@pytest.fixture(scope="module")
def app(basemodel_class: type[Any]) -> FastAPI:
    class ItemIn(basemodel_class):
        name: str
        value: int

    class ItemOut(basemodel_class):
        name: str
        value: int
        dep: int

    class LargeIn(basemodel_class):
        items: list[dict[str, Any]]
        metadata: dict[str, Any]

    class LargeOut(basemodel_class):
        items: list[dict[str, Any]]
        metadata: dict[str, Any]

    app = FastAPI()

    with warnings.catch_warnings(record=True):
        warnings.filterwarnings(
            "ignore",
            message=r"pydantic\.v1 is deprecated and will soon stop being supported by FastAPI\..*",
            category=DeprecationWarning,
        )

        @app.post("/sync/validated", response_model=ItemOut)
        def sync_validated(item: ItemIn, dep: Annotated[int, Depends(dep_b)]):
            return ItemOut(name=item.name, value=item.value, dep=dep)

        @app.get("/sync/dict-no-response-model")
        def sync_dict_no_response_model():
            return {"name": "foo", "value": 123}

        @app.get("/sync/dict-with-response-model", response_model=ItemOut)
        def sync_dict_with_response_model(
            dep: Annotated[int, Depends(dep_b)],
        ):
            return {"name": "foo", "value": 123, "dep": dep}

        @app.get("/sync/model-no-response-model")
        def sync_model_no_response_model(dep: Annotated[int, Depends(dep_b)]):
            return ItemOut(name="foo", value=123, dep=dep)

        @app.get("/sync/model-with-response-model", response_model=ItemOut)
        def sync_model_with_response_model(dep: Annotated[int, Depends(dep_b)]):
            return ItemOut(name="foo", value=123, dep=dep)

        @app.post("/async/validated", response_model=ItemOut)
        async def async_validated(
            item: ItemIn,
            dep: Annotated[int, Depends(dep_b)],
        ):
            return ItemOut(name=item.name, value=item.value, dep=dep)

        @app.post("/sync/large-receive")
        def sync_large_receive(payload: LargeIn):
            return {"received": len(payload.items)}

        @app.post("/async/large-receive")
        async def async_large_receive(payload: LargeIn):
            return {"received": len(payload.items)}

        @app.get("/sync/large-dict-no-response-model")
        def sync_large_dict_no_response_model():
            return LARGE_PAYLOAD

        @app.get("/sync/large-dict-with-response-model", response_model=LargeOut)
        def sync_large_dict_with_response_model():
            return LARGE_PAYLOAD

        @app.get("/sync/large-model-no-response-model")
        def sync_large_model_no_response_model():
            return LargeOut(items=LARGE_ITEMS, metadata=LARGE_METADATA)

        @app.get("/sync/large-model-with-response-model", response_model=LargeOut)
        def sync_large_model_with_response_model():
            return LargeOut(items=LARGE_ITEMS, metadata=LARGE_METADATA)

        @app.get("/async/large-dict-no-response-model")
        async def async_large_dict_no_response_model():
            return LARGE_PAYLOAD

        @app.get("/async/large-dict-with-response-model", response_model=LargeOut)
        async def async_large_dict_with_response_model():
            return LARGE_PAYLOAD

        @app.get("/async/large-model-no-response-model")
        async def async_large_model_no_response_model():
            return LargeOut(items=LARGE_ITEMS, metadata=LARGE_METADATA)

        @app.get("/async/large-model-with-response-model", response_model=LargeOut)
        async def async_large_model_with_response_model():
            return LargeOut(items=LARGE_ITEMS, metadata=LARGE_METADATA)

        @app.get("/async/dict-no-response-model")
        async def async_dict_no_response_model():
            return {"name": "foo", "value": 123}

        @app.get("/async/dict-with-response-model", response_model=ItemOut)
        async def async_dict_with_response_model(
            dep: Annotated[int, Depends(dep_b)],
        ):
            return {"name": "foo", "value": 123, "dep": dep}

        @app.get("/async/model-no-response-model")
        async def async_model_no_response_model(
            dep: Annotated[int, Depends(dep_b)],
        ):
            return ItemOut(name="foo", value=123, dep=dep)

        @app.get("/async/model-with-response-model", response_model=ItemOut)
        async def async_model_with_response_model(
            dep: Annotated[int, Depends(dep_b)],
        ):
            return ItemOut(name="foo", value=123, dep=dep)

    return app


@pytest.fixture(scope="module")
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


def _bench_get(benchmark, client: TestClient, path: str) -> tuple[int, bytes]:
    warmup = client.get(path)
    assert warmup.status_code == 200

    def do_request() -> tuple[int, bytes]:
        response = client.get(path)
        return response.status_code, response.content

    return benchmark(do_request)


def _bench_post_json(
    benchmark, client: TestClient, path: str, json: dict[str, Any]
) -> tuple[int, bytes]:
    warmup = client.post(path, json=json)
    assert warmup.status_code == 200

    def do_request() -> tuple[int, bytes]:
        response = client.post(path, json=json)
        return response.status_code, response.content

    return benchmark(do_request)


def test_sync_receiving_validated_pydantic_model(benchmark, client: TestClient) -> None:
    status_code, body = _bench_post_json(
        benchmark,
        client,
        "/sync/validated",
        json={"name": "foo", "value": 123},
    )
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_sync_return_dict_without_response_model(benchmark, client: TestClient) -> None:
    status_code, body = _bench_get(benchmark, client, "/sync/dict-no-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123}'


def test_sync_return_dict_with_response_model(benchmark, client: TestClient) -> None:
    status_code, body = _bench_get(benchmark, client, "/sync/dict-with-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_sync_return_model_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(benchmark, client, "/sync/model-no-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_sync_return_model_with_response_model(benchmark, client: TestClient) -> None:
    status_code, body = _bench_get(benchmark, client, "/sync/model-with-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_async_receiving_validated_pydantic_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_post_json(
        benchmark, client, "/async/validated", json={"name": "foo", "value": 123}
    )
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_async_return_dict_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(benchmark, client, "/async/dict-no-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123}'


def test_async_return_dict_with_response_model(benchmark, client: TestClient) -> None:
    status_code, body = _bench_get(benchmark, client, "/async/dict-with-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_async_return_model_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(benchmark, client, "/async/model-no-response-model")
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_async_return_model_with_response_model(benchmark, client: TestClient) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/async/model-with-response-model"
    )
    assert status_code == 200
    assert body == b'{"name":"foo","value":123,"dep":42}'


def test_sync_receiving_large_payload(benchmark, client: TestClient) -> None:
    status_code, body = _bench_post_json(
        benchmark,
        client,
        "/sync/large-receive",
        json=LARGE_PAYLOAD,
    )
    assert status_code == 200
    assert body == b'{"received":300}'


def test_async_receiving_large_payload(benchmark, client: TestClient) -> None:
    status_code, body = _bench_post_json(
        benchmark,
        client,
        "/async/large-receive",
        json=LARGE_PAYLOAD,
    )
    assert status_code == 200
    assert body == b'{"received":300}'


def _expected_large_payload_json_bytes() -> bytes:
    return json.dumps(
        LARGE_PAYLOAD,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def test_sync_return_large_dict_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/sync/large-dict-no-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_sync_return_large_dict_with_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/sync/large-dict-with-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_sync_return_large_model_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/sync/large-model-no-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_sync_return_large_model_with_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/sync/large-model-with-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_async_return_large_dict_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/async/large-dict-no-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_async_return_large_dict_with_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/async/large-dict-with-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_async_return_large_model_without_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/async/large-model-no-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()


def test_async_return_large_model_with_response_model(
    benchmark, client: TestClient
) -> None:
    status_code, body = _bench_get(
        benchmark, client, "/async/large-model-with-response-model"
    )
    assert status_code == 200
    assert body == _expected_large_payload_json_bytes()
