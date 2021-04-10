#!/usr/bin/env bash

set -e
set -x

poetry run python ./scripts/docs.py build-all
