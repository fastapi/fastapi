#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint.sh
# Check README.md is up to date
python ./scripts/docs.py verify-readme
export PYTHONPATH=./docs_src
pytest --cov=fastapi --cov=tests --cov=docs_src --cov-report=term-missing:skip-covered --cov-report=xml tests ${@}
