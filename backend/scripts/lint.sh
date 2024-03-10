#!/usr/bin/env bash

set -x

mypy app
ruff app
ruff format app --check
