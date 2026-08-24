#!/usr/bin/env bash
set -euo pipefail

# Gate: prevent deleting tests unless explicitly acknowledged in PR text.
# Rule: if any file under tests/ is deleted in this PR, require "DELETE_TESTS:" in PR title/body.

BASE_SHA="${GITHUB_BASE_SHA:-}"
HEAD_SHA="${GITHUB_SHA:-HEAD}"

if [[ -z "${BASE_SHA}" ]]; then
  echo "ERROR: GITHUB_BASE_SHA is not set. This script is intended for pull_request events."
  echo "Local test: set GITHUB_BASE_SHA to the base commit SHA (e.g., origin/main)."
  exit 2
fi

deleted_tests="$(
  git diff --name-status "${BASE_SHA}...${HEAD_SHA}" \
    | awk '$1 == "D" {print $2}' \
    | grep -E '^tests/' || true
)"

if [[ -z "${deleted_tests}" ]]; then
  echo "OK: no deleted files under tests/."
  exit 0
fi

echo "Detected deleted test files:"
echo "${deleted_tests}"

# Pull Request context (GitHub Actions provides these on pull_request events)
PR_TITLE="${PR_TITLE:-${GITHUB_PR_TITLE:-}}"
PR_BODY="${PR_BODY:-${GITHUB_PR_BODY:-}}"

combined="${PR_TITLE}"$'\n'"${PR_BODY}"

if echo "${combined}" | grep -qE 'DELETE_TESTS:\s*\S+'; then
  echo "OK: deletion acknowledged via DELETE_TESTS: <reason> in PR title/body."
  exit 0
fi

echo "FAIL: tests/ deletions require an explicit acknowledgement."
echo "Add to PR title or body a line like: DELETE_TESTS: <reason>"
exit 1