#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs_src fastapi tests scripts --exclude=__init__.py
black fastapi tests docs_src scripts
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --thirdparty fastapi --thirdparty pydantic --thirdparty starlette --apply fastapi tests docs_src scripts
