#!/usr/bin/env bash
set -x

ruff check fastapi tests docs_src scripts --fix
ruff format fastapi tests docs_src scripts
