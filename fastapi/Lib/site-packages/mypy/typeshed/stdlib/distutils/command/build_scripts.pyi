from typing import Any

from ..cmd import Command
from ..util import Mixin2to3 as Mixin2to3

first_line_re: Any

class build_scripts(Command):
    description: str
    user_options: Any
    boolean_options: Any
    build_dir: Any
    scripts: Any
    force: Any
    executable: Any
    outfiles: Any
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def get_source_files(self): ...
    def run(self) -> None: ...
    def copy_scripts(self): ...

class build_scripts_2to3(build_scripts, Mixin2to3):
    def copy_scripts(self): ...
