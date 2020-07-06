#!/usr/bin/env bash

set -e
set -x

mypy fastapi
black fastapi tests --check
isort . --check-only 
