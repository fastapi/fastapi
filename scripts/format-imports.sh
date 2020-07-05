#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports --thirdparty fastapi fastapi tests docs_src scripts
sh ./scripts/format.sh
