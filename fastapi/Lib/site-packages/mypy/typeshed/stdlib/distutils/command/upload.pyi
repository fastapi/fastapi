from typing import Any, ClassVar

from ..config import PyPIRCCommand

class upload(PyPIRCCommand):
    description: ClassVar[str]
    username: str
    password: str
    show_response: int
    sign: bool
    identity: Any
    def initialize_options(self) -> None: ...
    repository: Any
    realm: Any
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...
    def upload_file(self, command: str, pyversion: str, filename: str) -> None: ...
