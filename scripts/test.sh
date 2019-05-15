#!/usr/bin/env bash

set -e
set -x

# Remove temporary DB
if [ -f ./test.db ]; then
    rm ./test.db
fi

export PYTHONPATH=./docs/src
pytest --cov=fastapi --cov=tests --cov=docs/src --cov-report=term-missing ${@}
mypy fastapi --disallow-untyped-defs --follow-imports=skip
black fastapi tests --check
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --check-only --thirdparty fastapi fastapi tests
