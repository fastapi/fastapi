# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

**Install dependencies:**
```bash
pip install -e ".[all]"
pip install -r requirements-tests.txt
```

**Run tests:**
```bash
# Run all tests with coverage
./scripts/test.sh

# Run a single test file
coverage run -m pytest tests/test_application.py

# Run a specific test
coverage run -m pytest tests/test_application.py::test_app -v

# Note: PYTHONPATH=./docs_src is set by the test script for importing tutorial examples
```

**Linting and formatting:**
```bash
# Check linting (mypy + ruff)
./scripts/lint.sh

# Auto-fix and format
./scripts/format.sh

# Individual commands
mypy fastapi
ruff check fastapi tests docs_src scripts
ruff format fastapi tests
```

**Pre-commit hooks:** Uses `uv run` for ruff and docs generation hooks.

## Architecture Overview

FastAPI is built on top of **Starlette** (ASGI framework) and **Pydantic** (data validation).

### Core Module Structure (`fastapi/`)

- **`applications.py`** - `FastAPI` class extending Starlette's `Starlette` class. Contains app initialization, OpenAPI schema generation, and route registration methods (`get`, `post`, `put`, etc.)

- **`routing.py`** - `APIRouter` and `APIRoute` classes. Handles path operation decoration, request/response processing, and dependency injection integration. The `request_response` function wraps endpoints with `AsyncExitStack` for dependency lifecycle management.

- **`params.py`** - Parameter classes (`Query`, `Path`, `Header`, `Cookie`, `Body`, `Form`, `File`) extending Pydantic's `FieldInfo`. These define how request data is extracted and validated.

- **`param_functions.py`** - Function versions of parameter classes for use with `Annotated` typing pattern.

- **`dependencies/`** - Dependency injection system:
  - `models.py` - `Dependant` dataclass representing resolved dependency tree
  - `utils.py` - `get_dependant()` analyzes function signatures, `solve_dependencies()` resolves and caches dependencies at request time

- **`openapi/`** - OpenAPI/Swagger generation:
  - `utils.py` - `get_openapi()` generates OpenAPI schema from routes
  - `docs.py` - Swagger UI and ReDoc HTML generation
  - `models.py` - Pydantic models for OpenAPI spec

- **`security/`** - Security scheme implementations (OAuth2, API Key, HTTP Basic/Bearer)

- **`_compat/`** - Pydantic v2 compatibility layer

### Request Flow

1. Request hits `FastAPI` app (Starlette ASGI)
2. `APIRoute.handle()` matches route and calls endpoint wrapper
3. `solve_dependencies()` resolves dependency tree (with caching)
4. Parameters extracted from path/query/headers/body via `Param` classes
5. Pydantic validates all inputs
6. Endpoint function called with resolved dependencies
7. Response serialized through `jsonable_encoder`

### Testing Patterns

Tests use `TestClient` from Starlette (via `fastapi.testclient`). Test files in `tests/` mirror the structure of tutorials in `docs_src/`. Tests import example code from `docs_src/` to verify documentation examples work correctly.
