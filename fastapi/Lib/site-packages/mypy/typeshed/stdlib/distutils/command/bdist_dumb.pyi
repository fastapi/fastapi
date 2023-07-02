from typing import Any

from ..cmd import Command

class bdist_dumb(Command):
    description: str
    user_options: Any
    boolean_options: Any
    default_format: Any
    bdist_dir: Any
    plat_name: Any
    format: Any
    keep_temp: int
    dist_dir: Any
    skip_build: Any
    relative: int
    owner: Any
    group: Any
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...
