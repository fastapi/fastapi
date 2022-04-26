#!/usr/bin/env bash

set -e
set -x

env/bin/python -m mypy fastapi
env/bin/python -m flake8 fastapi tests
env/bin/python -m black fastapi tests --check
env/bin/python -m isort fastapi tests docs_src scripts --check-only
