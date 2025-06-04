
# Test file (AUEB DMST - Spinelis SEIP)
# by Joanna Karitsioti & George Tsakalos

import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

DATA_PATH = "dbase_examples"
API_PREFIX = ""

@pytest.mark.parametrize("format,expected_type,expected_header,filename,mimetype", [
    ("json", "application/json", None, "data_json.json", "application/json"),
    ("csv", "text/csv", "attachment; filename=data.csv", "data_csv.csv", "text/csv"),
    ("excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "attachment; filename=data.xlsx", "data_json.json", "application/json"),
    ("pdf", "application/pdf", "attachment; filename=data.pdf", "data_json.json", "application/json"),
    ("parquet", "application/octet-stream", "attachment; filename=data.parquet", "data_json.json", "application/json"),
])
def test_export_formats(format, expected_type, expected_header, filename, mimetype):
    filepath = os.path.join(DATA_PATH, filename)
    assert os.path.exists(filepath), f"Missing file: {filepath}"
    with open(filepath, "rb") as f:
        response = client.post(
            f"{API_PREFIX}/export?format={format}",
            files={"file": (filename, f.read(), mimetype)}
        )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(expected_type)
    if expected_header:
        assert response.headers.get("content-disposition") == expected_header


def test_sqlite_export():
    filepath = os.path.join(DATA_PATH, "data_json.json")
    assert os.path.exists(filepath), f"Missing file: {filepath}"
    with open(filepath, "rb") as f:
        response = client.post(
            f"{API_PREFIX}/export?format=sqlite",
            files={"file": ("data_json.json", f.read(), "application/json")}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-sqlite3"
    assert response.headers.get("content-disposition") == "attachment; filename=data_export.db"
    assert len(response.content) > 0


@pytest.mark.skipif(
    not all(os.getenv(key) for key in ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]),
    reason="MySQL env vars not set"
)
def test_mysql_export():
    filepath = os.path.join(DATA_PATH, "data_json.json")
    assert os.path.exists(filepath), f"Missing file: {filepath}"
    with open(filepath, "rb") as f:
        response = client.post(
            f"{API_PREFIX}/export?format=mysql",
            files={"file": ("data_json.json", f.read(), "application/json")}
        )
    assert response.status_code == 200
    assert response.json().get("message", "").startswith("Data successfully exported to MySQL.")


def test_root_redirects_to_docs():
    response = client.get(f"{API_PREFIX}/")
    assert response.status_code in (307, 200)
