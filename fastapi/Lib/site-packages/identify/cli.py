from __future__ import annotations

import argparse
import json
from typing import Sequence

from identify import identify


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename-only", action="store_true")
    parser.add_argument("path")
    args = parser.parse_args(argv)

    if args.filename_only:
        func = identify.tags_from_filename
    else:
        func = identify.tags_from_path

    try:
        tags = sorted(func(args.path))
    except ValueError as e:
        print(e)
        return 1

    if not tags:
        return 1
    else:
        print(json.dumps(tags))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
