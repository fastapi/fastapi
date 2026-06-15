#!/usr/bin/env bash

set -e
set -x

mypy fastapi
ty check fastapi docs_src --force-exclude
ruff check fastapi tests docs_src scripts
ruff format fastapi tests --check
