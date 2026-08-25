from sandbox.log_summariser.app.main import app, STORE, SummaryRecord
from fastapi.testclient import TestClient


def test_get_summary_happy_path_and_404():
    client = TestClient(app)

    # Seed store
    STORE.clear()
    STORE.setdefault("t1", {})["s1"] = SummaryRecord(job_status="succeeded", summary_text="ok")

    # Happy path
    r = client.get("/tenants/t1/summaries/s1")
    assert r.status_code == 200
    assert r.json() == {"job_status": "succeeded", "summary_text": "ok", "error": None}

    # Missing summary
    r2 = client.get("/tenants/t1/summaries/missing")
    assert r2.status_code == 404
    assert r2.json()["error"]["code"] == "not_found"

    # Missing tenant
    r3 = client.get("/tenants/missing/summaries/s1")
    assert r3.status_code == 404
    assert r3.json()["error"]["code"] == "not_found"


