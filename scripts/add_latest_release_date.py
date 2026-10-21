"""Check release-notes.md and add today's date to the latest release header if missing."""

import re
import sys
from datetime import date

RELEASE_NOTES_FILE = "docs/en/docs/release-notes.md"
RELEASE_HEADER_PATTERN = re.compile(r"^## (\d+\.\d+\.\d+)\s*(\(.*\))?\s*$")


def main() -> None:
    with open(RELEASE_NOTES_FILE) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        match = RELEASE_HEADER_PATTERN.match(line)
        if not match:
            continue

        version = match.group(1)
        date_part = match.group(2)

        if date_part:
            print(f"Latest release {version} already has a date: {date_part}")
            sys.exit(0)

        today = date.today().isoformat()
        lines[i] = f"## {version} ({today})\n"
        print(f"Added date: {version} ({today})")

        with open(RELEASE_NOTES_FILE, "w") as f:
            f.writelines(lines)
        sys.exit(0)

    print("No release header found")
    sys.exit(1)


if __name__ == "__main__":
    main()
