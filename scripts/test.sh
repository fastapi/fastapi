#!/usr/bin/env bash

set -e
set -x

# Remove temporary DB
if [ -f ./test.db ]; then
    rm ./test.db
fi

export PYTHONPATH=./docs/src
pytest --cov=fastapi --cov=tests --cov=docs/src --cov-report=term-missing ${@}
bash ./scripts/lint.sh
# Check README.md is up to date
diff --brief docs/index.md README.md
