#!/usr/bin/env bash

set -e
set -x

mypy app
ruff app
ruff format app --check
