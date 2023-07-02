from __future__ import annotations

import sys
from typing import Sequence

from pre_commit import output


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    for arg in argv:
        output.write_line(arg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
