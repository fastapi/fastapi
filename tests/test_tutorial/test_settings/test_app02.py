from fastapi.testclient import TestClient

from docs_src.settings.app02 import main, test_main

client = TestClient(main.app)


def test_setting_override():
    test_main.test_app()
