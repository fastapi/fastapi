# Governance — fastapi
# Inferred by crag analyze — review and adjust as needed

## Identity
- Project: fastapi
- Stack: python

## Gates (run in order, stop on failure)
### Lint
- uv run mypy .

### Test
- uv run pytest

### Build
- python -m build

### CI (inferred from workflow)
- python -m build --sdist
- uv run --no-sync bash scripts/test-cov.sh
- uv run --no-sync pytest tests/benchmarks --codspeed
- uv run coverage combine coverage
- uv run coverage html --title "Coverage for ${{ github.sha }}"
- uv run coverage report --fail-under=100

## Advisories (informational, not enforced)
- actionlint  # [ADVISORY]

## Branch Strategy
- Trunk-based development
- Free-form commits
- Commit trailer: Co-Authored-By: Claude <noreply@anthropic.com>

## Security
- No hardcoded secrets — grep for sk_live, AKIA, password= before commit

## Autonomy
- Auto-commit after gates pass

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

## Dependencies
- Package manager: uv (uv.lock)

## Anti-Patterns

Do not:
- Do not catch bare `Exception` — catch specific exceptions
- Do not use mutable default arguments (e.g., `def f(x=[])`)
- Do not use `import *` — use explicit imports
