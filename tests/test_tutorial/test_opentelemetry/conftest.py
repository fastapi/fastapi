import os

import pytest


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    for name in os.environ:
        if name.startswith(("OTEL_", "LOGFIRE_", "SENTRY_")):
            monkeypatch.delenv(name)
