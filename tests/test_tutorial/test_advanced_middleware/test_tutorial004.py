from fastapi.testclient import TestClient

from docs_src.advanced_middleware.tutorial004 import app

client = TestClient(app)


def test_app_middleware_called_once(capsys):
    r = client.get("/")
    assert r.status_code == 200

    captured = capsys.readouterr().out
    assert captured.count("App before") == 1
    assert captured.count("Outer before") == 0
    assert captured.count("Handler") == 1
    assert captured.count("Outer after") == 0
    assert captured.count("App after") == 1


def test_outer_middleware_called_once(capsys):
    r = client.get("/outer/")
    assert r.status_code == 200

    captured = capsys.readouterr().out
    assert captured.count("App before") == 1
    assert captured.count("Outer before") == 1
    assert captured.count("Handler") == 1
    assert captured.count("Outer after") == 1
    assert captured.count("App after") == 1


def test_name_middleware_called_once(capsys):
    name = "you"
    r = client.get(f"/outer/inner/{name}")
    assert r.status_code == 200
    assert r.json() == {"message": f"Hello {name} from inner!"}

    captured = capsys.readouterr().out
    seq = [
        "App before",
        "Outer before",
        f"Hi {name}!",
        "Handler",
        f"Bye {name}!",
        "Outer after",
        "App after",
    ]
    for msg in seq:
        assert captured.count(msg) == 1

    idx = 0
    for msg in seq:
        next_idx = captured.find(msg, idx)
        assert next_idx >= idx
        idx = next_idx
