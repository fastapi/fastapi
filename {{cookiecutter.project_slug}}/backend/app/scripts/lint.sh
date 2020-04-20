#!/usr/bin/env bash

set -x

mypy app
black app --check
isort --recursive --check-only app
vulture app --min-confidence 70
flake8
