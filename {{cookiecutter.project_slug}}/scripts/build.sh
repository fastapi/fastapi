#! /usr/bin/env sh

# Exit in case of error
set -e

TAG=${TAG} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
docker-compose \
-f docker-compose.deploy.build.yml \
-f docker-compose.deploy.images.yml \
config > docker-stack.yml

docker-compose -f docker-stack.yml build
