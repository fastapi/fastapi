#! /usr/bin/env bash

set -x
set -e

INPUT_PR1=${INPUT_PR1:?Variable not set}
INPUT_PR2=${INPUT_PR2:?Variable not set}
INPUT_PR3=${INPUT_PR3:?Variable not set}
echo "$INPUT_PR1"
echo "$INPUT_PR2"
echo "$INPUT_PR3"
INPUT_NAME=${INPUT_NAME:?Variable not set}
INPUT_GITHUB_TOKEN=${INPUT_GITHUB_TOKEN:?Variable not set}

# curl \
#   -X POST \
#   -H "Authorization: token ${INPUT_GITHUB_TOKEN}" \
#   -H "Accept: application/vnd.github.v3+json" \
#   https://api.github.com/repos/tiangolo/fastapi/actions/workflows/preview-docs.yml/dispatches \
#   -d '{"ref":"master", "inputs": {"pr": "'"${INPUT_PR}"'", "name": "'"${INPUT_NAME}"'"}}'
