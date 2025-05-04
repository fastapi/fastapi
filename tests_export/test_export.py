import sys
import pytest

# Automatically skip the whole test file if required libraries are missing
missing_deps = []
for lib in ["pandas", "httpx", "pyarrow", "reportlab", "avro", "mysql.connector"]:
    try:
        __import__(lib)
    except ImportError:
        missing_deps.append(lib)
if missing_deps:
    pytest.skip(
        f"Skipping export tests because dependencies are missing: {', '.join(missing_deps)}",
        allow_module_level=True
    )

from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from fastapi.contrib.export.routes import router as export_router



    
app = FastAPI()
app.include_router(export_router)

transport = ASGITransport(app=app)

@pytest.mark.asyncio
@pytest.mark.parametrize("export_format,expected_media_type", [
    ("json", "application/json"),
    ("csv", "text/csv"),
    ("excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    ("pdf", "application/pdf"),
    ("parquet", "application/octet-stream"),
    ("feather", "application/octet-stream"),
])
async def test_export_formats(export_format, expected_media_type):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/export?format={export_format}")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith(expected_media_type)
        if export_format != "json":
            assert "attachment" in response.headers.get("content-disposition", "")

@pytest.mark.asyncio
async def test_export_invalid_format():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/export?format=invalid")
        assert response.status_code == 400
        assert response.json()["error"] == "Invalid format"
