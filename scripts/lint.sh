#!/usr/bin/env bash

set -e
set -x

mypy fastapi
ruff fastapi tests docs_src scripts
black fastapi tests --check
isort fastapi tests docs_src scripts --check-only
