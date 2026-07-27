import sys

import pytest

from tests.benchmarks.utils import (
    ROUTE_COUNT,
    ROUTE_PATH_PREFIX,
    create_openapi_app,
    generate_openapi,
)

if "--codspeed" not in sys.argv:
    pytest.skip(
        "Benchmark tests are skipped by default; run with --codspeed.",
        allow_module_level=True,
    )


@pytest.mark.timeout(60)
def test_openapi_dependency_graph(benchmark) -> None:
    app = create_openapi_app()
    schema = benchmark(generate_openapi, app)
    dynamic_paths = [
        path for path in schema["paths"] if path.startswith(ROUTE_PATH_PREFIX)
    ]
    assert len(dynamic_paths) == ROUTE_COUNT
    assert all(
        any(
            parameter["in"] == "query" and parameter["name"] == "query_value"
            for parameter in schema["paths"][path]["get"]["parameters"]
        )
        for path in dynamic_paths
    )
