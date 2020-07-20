#! /usr/bin/env bash

set -x
set -e

PR=${PR:?Variable not set}
DEPLOY_URL=${DEPLOY_URL:?Variable not set}
GITHUB_TOKEN=${GITHUB_TOKEN:?Variable not set}
COMMIT=${COMMIT:?Variable not set}

curl \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    https://api.github.com/repos/tiangolo/fastapi/issues/${PR}/comments \
    -d '{"body": "📝 Docs preview for commit '"${COMMIT} at: ${DEPLOY_URL}"'"}'
