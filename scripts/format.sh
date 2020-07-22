#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs_src fastapi tests scripts --exclude=__init__.py
flake8 fastapi tests docs_src scripts --max-line-length=88 --select=C,E,F,W,B,B950 --ignore=E203,E501,W503
black fastapi tests docs_src scripts
isort fastapi tests docs_src scripts
