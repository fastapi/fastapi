---
trigger: always_on
description: Governance rules for fastapi — compiled from governance.md by crag
---

# Windsurf Rules — fastapi

Generated from governance.md by crag. Regenerate: `crag compile --target windsurf`

## Project

(No description)

**Stack:** python

## Runtimes

python

## Cascade Behavior

When Windsurf's Cascade agent operates on this project:

- **Always read governance.md first.** It is the single source of truth for quality gates and policies.
- **Run all mandatory gates before proposing changes.** Stop on first failure.
- **Respect classifications.** OPTIONAL gates warn but don't block. ADVISORY gates are informational.
- **Respect path scopes.** Gates with a `path:` annotation must run from that directory.
- **No destructive commands.** Never run rm -rf, dd, DROP TABLE, force-push to main, curl|bash, docker system prune.
- - No hardcoded secrets — grep for sk_live, AKIA, password= before commit
- Follow the project commit conventions.

## Quality Gates (run in order)

1. `uv run mypy .`
2. `uv run pytest`
3. `python -m build`
4. `python -m build --sdist`
5. `uv run --no-sync bash scripts/test-cov.sh`
6. `uv run --no-sync pytest tests/benchmarks --codspeed`
7. `uv run coverage combine coverage`
8. `uv run coverage html --title "Coverage for ${{ github.sha }}"`
9. `uv run coverage report --fail-under=100`

## Rules of Engagement

1. **Minimal changes.** Don't rewrite files that weren't asked to change.
2. **No new dependencies** without explicit approval.
3. **Prefer editing** existing files over creating new ones.
4. **Always explain** non-obvious changes in commit messages.
5. **Ask before** destructive operations (delete, rename, migrate schema).

---

**Tool:** crag — https://www.npmjs.com/package/@whitehatd/crag
