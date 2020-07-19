#! /usr/bin/env bash

set -x
set -e

PR1=${PR1:?Variable not set}
PR2=${PR2:?Variable not set}
PR3=${PR3:?Variable not set}
PR4=${PR4:?Variable not set}
echo "$PR1"
echo "$PR2"
echo "$PR3"
echo "$PR4"
NAME=${NAME:?Variable not set}
GITHUB_TOKEN=${GITHUB_TOKEN:?Variable not set}

# curl \
#   -X POST \
#   -H "Authorization: token ${INPUT_GITHUB_TOKEN}" \
#   -H "Accept: application/vnd.github.v3+json" \
#   https://api.github.com/repos/tiangolo/fastapi/actions/workflows/preview-docs.yml/dispatches \
#   -d '{"ref":"master", "inputs": {"pr": "'"${INPUT_PR}"'", "name": "'"${INPUT_NAME}"'"}}'
