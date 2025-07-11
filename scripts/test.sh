#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=./docs_src
coverage run -m pytest tests ${@}
