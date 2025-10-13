#!/bin/bash
set -e

# Usage: ./test.sh base   # runs baseline tests
#        ./test.sh new    # runs newly added tests (must fail before solution)

if [[ "$1" == "base" ]]; then
    # Run only your baseline/existing tests
    pytest tests/existing_tests.py
elif [[ "$1" == "new" ]]; then
    # Run the newly-added tests expected to fail before bugfix
    pytest tests/test_form_defaults.py
else
    echo "Usage: ./test.sh {base|new}"
    exit 1
fi
