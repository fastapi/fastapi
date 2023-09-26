#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=./docs_src
export SQLALCHEMY_SILENCE_UBER_WARNING=1
coverage run -m pytest tests ${@} -W ignore::DeprecationWarning
