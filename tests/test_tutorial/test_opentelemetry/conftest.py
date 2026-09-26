import pytest

from tests.test_telemetry.conftest import remove_export_environment


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    remove_export_environment(monkeypatch)
