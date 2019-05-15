#!/usr/bin/env bash

set -e
set -x

export VERSION_SCRIPT="import sys; print('%s.%s' % sys.version_info[0:2])"
export PYTHON_VERSION=`python -c "$VERSION_SCRIPT"`

# Remove temporary DB
if [ -f ./test.db ]; then
    rm ./test.db
fi

export PYTHONPATH=./docs/src
pytest --cov=fastapi --cov=tests --cov=docs/src --cov-report=term-missing ${@}
mypy fastapi --disallow-untyped-defs --follow-imports=skip
black fastapi tests --check
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --check-only --thirdparty fastapi fastapi tests
