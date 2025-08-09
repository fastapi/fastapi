#!/usr/bin/env bash

set -e
set -x

mypy fastapi
ruff check fastapi tests docs_src scripts
ruff format fastapi tests --check
