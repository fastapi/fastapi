#!/usr/bin/env bash

set -e
set -x

mypy fastapi
flake8 fastapi tests --max-line-length=88 --select=C,E,F,W,B,B950 --ignore=E203,E501,W503
black fastapi tests --check
isort fastapi tests docs_src scripts --check-only
