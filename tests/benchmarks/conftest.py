import pytest


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    # Benchmarks are intentionally skipped unless explicitly requested with --codspeed
    # to avoid slowing down regular test runs, and to run them only on
    # supported Python versions (e.g. Pydantic v1 only up to Python 3.13).
    run_codspeed = bool(getattr(config.option, "codspeed", False))

    if run_codspeed:
        return

    skip_marker = pytest.mark.skip(
        reason="Benchmark tests are skipped by default; run with --codspeed."
    )

    for item in items:
        item.add_marker(skip_marker)
