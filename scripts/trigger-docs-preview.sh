#! /usr/bin/env bash

set -x
set -e

PR=${PR}

if [ -z "$PR" ]; then
    echo "Not a PR build, skip trigger docs preview"
    exit 0
fi

NAME=${NAME:?Variable not set}
GITHUB_TOKEN=${GITHUB_TOKEN:?Variable not set}

curl \
  -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/tiangolo/fastapi/actions/workflows/preview-docs.yml/dispatches \
  -d '{"ref":"master", "inputs": {"pr": "'"${PR}"'", "name": "'"${NAME}"'"}}'
