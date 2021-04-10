#!/bin/sh -e
set -x

poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs_src fastapi tests scripts --exclude=__init__.py
poetry run black fastapi tests docs_src scripts
poetry run isort fastapi tests docs_src scripts
