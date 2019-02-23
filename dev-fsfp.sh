#! /usr/bin/env bash

# Exit in case of error
set -e

rm -rf ./dev-fsfp

cookiecutter --config-file ./full-stack-fastapi-postgresql/dev-fsfp-config.yml --no-input -f ./full-stack-fastapi-postgresql
