#!/bin/sh -e
set -x

black fastapi tests
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --apply fastapi tests
