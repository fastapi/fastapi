#! /usr/bin/env bash

# Run this script from outside the project, to integrate a dev-fsfp project with changes and review modifications

# Exit in case of error
set -e

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find ./dev-fsfp/ -type d -name __pycache__ -exec rm -r {} \+
fi

rm -rf ./full-stack-fastapi-postgresql/\{\{cookiecutter.project_slug\}\}/*

rsync -a --exclude=node_modules ./dev-fsfp/* ./full-stack-fastapi-postgresql/\{\{cookiecutter.project_slug\}\}/

rsync -a ./dev-fsfp/{.env,.gitignore,.gitlab-ci.yml} ./full-stack-fastapi-postgresql/\{\{cookiecutter.project_slug\}\}/
