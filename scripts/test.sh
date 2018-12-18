#!/usr/bin/env bash

set -e
set -x

export VERSION_SCRIPT="import sys; print('%s.%s' % sys.version_info[0:2])"
export PYTHON_VERSION=`python -c "$VERSION_SCRIPT"`

export PYTHONPATH=./docs/tutorial/src
# PYTHONPATH=. pytest --cov=fastapi --cov=tests --cov-fail-under=100 --cov-report=term-missing ${@} --cov-report=html
pytest --cov=fastapi --cov=tests --cov=docs/tutorial/src --cov-report=term-missing ${@} --cov-report=html
mypy fastapi --disallow-untyped-defs
if [ "${PYTHON_VERSION}" = '3.7' ]; then
    echo "Skipping 'black' on 3.7. See issue https://github.com/ambv/black/issues/494"
else
    black fastapi tests --check
fi
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --check-only fastapi tests
