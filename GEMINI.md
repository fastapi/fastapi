<!-- crag:auto-start -->
# GEMINI.md

> Generated from governance.md by crag. Regenerate: `crag compile --target gemini`

## Project Context

- **Name:** fastapi
- **Stack:** python
- **Runtimes:** python

## Rules

### Quality Gates

Run these checks in order before committing any changes:

1. [lint] `uv run mypy .`
2. [test] `uv run pytest`
3. [build] `python -m build`
4. [ci (inferred from workflow)] `python -m build --sdist`
5. [ci (inferred from workflow)] `uv run --no-sync bash scripts/test-cov.sh`
6. [ci (inferred from workflow)] `uv run --no-sync pytest tests/benchmarks --codspeed`
7. [ci (inferred from workflow)] `uv run coverage combine coverage`
8. [ci (inferred from workflow)] `uv run coverage html --title "Coverage for ${{ github.sha }}"`
9. [ci (inferred from workflow)] `uv run coverage report --fail-under=100`

### Security

- No hardcoded secrets — grep for sk_live, AKIA, password= before commit

### Workflow

- Follow project commit conventions
- Run quality gates before committing
- Review security implications of all changes

<!-- crag:auto-end -->
