#! /usr/bin/env bash

set -x
set -e

if [ -f docs.zip ]; then
    rm -rf docs.zip
fi
zip -r docs.zip ./site
