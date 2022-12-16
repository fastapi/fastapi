#!/bin/sh -e
set -x

ruff fastapi tests docs_src scripts --fix
black fastapi tests docs_src scripts
isort fastapi tests docs_src scripts
