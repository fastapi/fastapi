#!/usr/bin/env bash

set -e
set -x

mypy fastapi
ty check
ruff check fastapi tests docs_src scripts
ruff format fastapi tests --check
