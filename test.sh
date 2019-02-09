#! /usr/bin/env bash

# Exit in case of error
set -e

rm -rf ./testing-project

cookiecutter --config-file ./testing-config.yml --no-input -f ./

cd ./testing-project

bash ./scripts/test.sh

cd ../
