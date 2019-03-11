#! /usr/bin/env bash

# Run this script from outside the project, to generate a dev-fsfp project

# Exit in case of error
set -e

rm -rf ./dev-fsfp

cookiecutter --config-file ./full-stack-fastapi-postgresql/dev-fsfp-config.yml --no-input -f ./full-stack-fastapi-postgresql
