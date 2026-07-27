#!/usr/bin/env bash

set -e
set -x

bash scripts/test-cov.sh --cov-report=term-missing --cov-report=html ${@}
