#!/usr/bin/env bash

set -e

bash scripts/publish.sh

bash scripts/trigger-docker.sh

python scripts/gitter_releases_bot.py
