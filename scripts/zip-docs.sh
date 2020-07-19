#! /usr/bin/env bash

set -x
set -e

cd ./site/ || exit 1
zip -r docs.zip ./*
mv ./docs.zip ../
