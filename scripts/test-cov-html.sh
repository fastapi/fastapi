#!/usr/bin/env bash

set -e
set -x

bash scripts/test.sh ${@}
coverage combine
coverage report
coverage html
