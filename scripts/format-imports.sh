#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort fastapi tests docs_src scripts --force-single-line-imports
sh ./scripts/format.sh
