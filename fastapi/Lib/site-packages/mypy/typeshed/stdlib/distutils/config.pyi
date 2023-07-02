from abc import abstractmethod
from distutils.cmd import Command
from typing import ClassVar

DEFAULT_PYPIRC: str

class PyPIRCCommand(Command):
    DEFAULT_REPOSITORY: ClassVar[str]
    DEFAULT_REALM: ClassVar[str]
    repository: None
    realm: None
    user_options: ClassVar[list[tuple[str, str | None, str]]]
    boolean_options: ClassVar[list[str]]
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    @abstractmethod
    def run(self) -> None: ...
