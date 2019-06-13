#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --thirdparty fastapi --apply fastapi tests docs/src
sh ./scripts/format.sh
