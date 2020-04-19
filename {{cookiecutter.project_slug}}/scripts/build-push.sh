#! /usr/bin/env sh

# Exit in case of error
set -e

TAG=${TAG} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
. ./scripts/build.sh

docker-compose -f docker-compose.yml push
