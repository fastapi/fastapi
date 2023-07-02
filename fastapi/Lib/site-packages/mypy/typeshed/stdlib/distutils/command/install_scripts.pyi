from typing import Any

from ..cmd import Command

class install_scripts(Command):
    description: str
    user_options: Any
    boolean_options: Any
    install_dir: Any
    force: int
    build_dir: Any
    skip_build: Any
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    outfiles: Any
    def run(self) -> None: ...
    def get_inputs(self): ...
    def get_outputs(self): ...
