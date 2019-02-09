#! /usr/bin/env bash

# Exit in case of error
set -e

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker-compose \
    -f docker-compose.test.yml \
    -f docker-compose.shared.admin.yml \
    -f docker-compose.shared.base-images.yml \
    -f docker-compose.shared.depends.yml \
    -f docker-compose.shared.env.yml \
    -f docker-compose.dev.build.yml \
    -f docker-compose.dev.env.yml \
    -f docker-compose.dev.labels.yml \
    -f docker-compose.dev.networks.yml \
    -f docker-compose.dev.ports.yml \
    -f docker-compose.dev.volumes.yml \
    config > docker-stack.yml

#    -f docker-compose.dev.command.yml \

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -T backend-tests /tests-start.sh
