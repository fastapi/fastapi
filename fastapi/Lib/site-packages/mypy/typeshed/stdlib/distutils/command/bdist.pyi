from typing import Any

from ..cmd import Command

def show_formats() -> None: ...

class bdist(Command):
    description: str
    user_options: Any
    boolean_options: Any
    help_options: Any
    no_format_option: Any
    default_format: Any
    format_commands: Any
    format_command: Any
    bdist_base: Any
    plat_name: Any
    formats: Any
    dist_dir: Any
    skip_build: int
    group: Any
    owner: Any
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...
