#! /usr/bin/env bash

set -x
set -e

if [ -d ./site/ ]; then
    rm -rf ./site/
fi
unzip archive.zip
# Double zipped by GitHub when downlading the archive
unzip docs.zip
rm -rf archive.zip
rm -rf docs.zip
