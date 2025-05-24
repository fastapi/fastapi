
import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("format,expected_type,expected_header", [
    ("json", "application/json", None),
    ("csv", "text/csv", "attachment; filename=data.csv"),
    ("excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "attachment; filename=data.xlsx"),
    ("pdf", "application/pdf", "attachment; filename=data.pdf"),
    ("parquet", "application/octet-stream", "attachment; filename=data.parquet"),
])
def test_export_formats(format, expected_type, expected_header):
    response = client.get(f"/export?format={format}")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(expected_type)
    if expected_header:
        assert response.headers.get("content-disposition") == expected_header

def test_sqlite_export():
    response = client.get("/export?format=sqlite")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-sqlite3"
    assert response.headers.get("content-disposition") == "attachment; filename=data_export.db"
    assert len(response.content) > 0

@pytest.mark.skipif(
    not all(os.getenv(key) for key in ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]),
    reason="MySQL env vars not set"
)
def test_mysql_export():
    response = client.get("/export?format=mysql")
    assert response.status_code == 200
    assert response.json().get("message", "").startswith("Data successfully exported to MySQL.")

def test_root_redirects_to_docs():
    response = client.get("/")
    assert response.status_code in (307, 200)
