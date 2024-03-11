#! /usr/bin/env sh

# Exit in case of error
set -e
set -x

docker compose build
docker compose down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker compose up -d
docker compose exec -T backend bash /app/tests-start.sh "$@"
docker compose down -v --remove-orphans
