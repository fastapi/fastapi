from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from docs_src.handling_errors import tutorial008
from docs_src.handling_errors.tutorial008 import app

client = TestClient(app)


def test_unsupported_file_type(tmp_path: Path):
    file = tmp_path / "test.txt"
    file.write_text("<file content>")
    with open(file, "+rb") as fp:
        response = client.post(
            "/upload",
            files={"file": ("test.txt", fp, "text/plain")},
        )
    assert response.status_code == 415, response.text
    assert response.json() == {
        "error": "Unsupported file type",
        "hint": "Need help? Contact support@example.com",
    }


def test_file_too_large(tmp_path: Path):
    file = tmp_path / "test.pdf"
    file.write_text("<file content>" * 100)  # ~1.37 kB
    with patch.object(
        tutorial008,
        "MAX_FILE_SIZE_MB",
        new=0.001,  # MAX_FILE_SIZE_MB = 1 kB
    ):
        with open(file, "+rb") as fp:
            response = client.post(
                "/upload",
                files={"file": ("test.pdf", fp, "application/pdf")},
            )
    assert response.status_code == 413, response.text
    assert response.json() == {
        "error": "The uploaded file is too large.",
        "hint": "Need help? Contact support@example.com",
    }


def test_success(tmp_path: Path):
    file = tmp_path / "test.pdf"
    file.write_text("<file content>")
    with open(file, "+rb") as fp:
        response = client.post(
            "/upload",
            files={"file": ("test.pdf", fp, "application/pdf")},
        )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "filename": "test.pdf",
        "message": "File uploaded successfully!",
    }
