#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=./docs_src
pytest -n auto --dist loadgroup  tests scripts/tests/ ${@}
