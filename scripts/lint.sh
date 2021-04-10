#!/usr/bin/env bash

set -e
set -x

poetry run mypy fastapi
poetry run flake8 fastapi tests
poetry run black fastapi tests --check
poetry run isort fastapi tests docs_src scripts --check-only
