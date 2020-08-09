#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs_src fastapi tests scripts --exclude=__init__.py
black fastapi tests docs_src scripts
isort fastapi tests docs_src scripts
