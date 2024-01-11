#!/usr/bin/env bash

set -e
set -x

mypy fastapi
ruff fastapi tests docs_src scripts
ruff format fastapi tests --check
