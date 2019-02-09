#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=backend \
docker-compose \
-f docker-compose.shared.base-images.yml \
-f docker-compose.shared.env.yml \
-f docker-compose.shared.depends.yml \
-f docker-compose.deploy.build.yml \
-f docker-compose.test.yml \
config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -T backend-tests /tests-start.sh
docker-compose -f docker-stack.yml down -v --remove-orphans
