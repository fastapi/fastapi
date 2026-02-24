#!/usr/bin/env bash

set -e
set -x

bash scripts/test.sh --cov --cov-context=test --cov-report=term-missing --cov-report=html ${@}
