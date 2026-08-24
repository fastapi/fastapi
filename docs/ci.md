```md

\## Gate: no-test-deletions (`.github/workflows/no-test-deletions.yml`)

This gate blocks pull requests that delete any files under `tests/` unless the PR title or body contains an explicit acknowledgement line: `DELETE\_TESTS: <reason>`.



\*\*Why it exists (AI-assisted PRs):\*\* local hooks and “the agent checked” are not enforceable. This server-side required check ensures test deletions are always conscious and reviewable regardless of the author’s tooling or configuration.



\*\*What it does NOT catch:\*\* it does not validate test quality, coverage, or that new tests were added for new behavior—it only prevents silent deletion of existing tests.



\*\*Limitation:\*\* it relies on PR metadata (title/body). Engineers must remember to add the `DELETE\_TESTS:` line when deletions are intentional.



\### Admin step (make required)

GitHub: \*\*Settings → Branches → Branch protection rules → (master) → Require status checks to pass → add `no-test-deletions`\*\*.

```

