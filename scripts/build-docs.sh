#!/usr/bin/env bash

mkdocs build

cp ./docs/index.md ./README.md
