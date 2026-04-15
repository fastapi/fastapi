<!-- crag:auto-start -->
# AGENTS.md

> Generated from governance.md by crag. Regenerate: `crag compile --target agents-md`

## Project: fastapi


## Quality Gates

All changes must pass these checks before commit:

### Lint
1. `uv run mypy .`

### Test
1. `uv run pytest`

### Build
1. `python -m build`

### Ci (inferred from workflow)
1. `python -m build --sdist`
2. `uv run --no-sync bash scripts/test-cov.sh`
3. `uv run --no-sync pytest tests/benchmarks --codspeed`
4. `uv run coverage combine coverage`
5. `uv run coverage html --title "Coverage for ${{ github.sha }}"`
6. `uv run coverage report --fail-under=100`

## Coding Standards

- Stack: python
- Follow project commit conventions

## Architecture

- Type: monolith

## Key Directories

- `.github/` — CI/CD
- `docs/` — documentation
- `scripts/` — tooling
- `tests/` — tests

## Testing

- Framework: pytest
- Layout: flat
- Naming: test_*.py

## Anti-Patterns

Do not:
- Do not catch bare `Exception` — catch specific exceptions
- Do not use mutable default arguments (e.g., `def f(x=[])`)
- Do not use `import *` — use explicit imports

## Security

- No hardcoded secrets — grep for sk_live, AKIA, password= before commit

## Workflow

1. Read `governance.md` at the start of every session — it is the single source of truth.
2. Run all mandatory quality gates before committing.
3. If a gate fails, fix the issue and re-run only the failed gate.
4. Use the project commit conventions for all changes.

<!-- crag:auto-end -->
