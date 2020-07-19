#! /usr/bin/env bash

set -x
set -e

if [ -d ./site/ ]; then
    rm -rf ./site/
fi
unzip docs.zip
