from __future__ import annotations

import os.path

from pre_commit import output
from pre_commit.store import Store
from pre_commit.util import rmtree


def clean(store: Store) -> int:
    legacy_path = os.path.expanduser("~/.pre-commit")
    for directory in (store.directory, legacy_path):
        if os.path.exists(directory):
            rmtree(directory)
            output.write_line(f"Cleaned {directory}.")
    return 0
