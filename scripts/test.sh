#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint.sh
# Check README.md is up to date
diff --brief docs/en/docs/index.md README.md
export PYTHONPATH=./docs_src
pytest --cov=fastapi --cov=tests --cov=docs_src --cov-report=term-missing:skip-covered --cov-report=xml tests ${@}
