#!/usr/bin/env bash

set -e

bash scripts/publish.sh

bash scripts/trigger-docker.sh
