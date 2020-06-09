import fastapi



def test_fastapi_module_exports():
    """
    Test the publicly exported module set.
    Benefits for declaring explicitly the public exports:
        * Using __all__ sets what gets imported with `from fastapi import *`
        * Enables mypy to pass all checks with fastapi when using `implicit_reexport = False` 
    """

    missing = set(n for n in fastapi.__all__ if not getattr(fastapi, n, None))
    assert not missing, f"__all__ contains unresolved names: {missing}"
    assert fastapi.__all__ == [
        "status",
        "FastAPI",
        "BackgroundTasks",
        "UploadFile",
        "HTTPException",
        "Body",
        "Cookie",
        "Depends",
        "File",
        "Form",
        "Header",
        "Path",
        "Query",
        "Security",
        "Request",
        "Response",
        "APIRouter",
        "StaticFiles",
        "Jinja2Templates",
        "TestClient",
        "WebSocket",
    ]
