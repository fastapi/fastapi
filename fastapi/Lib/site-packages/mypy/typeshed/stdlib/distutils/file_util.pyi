from collections.abc import Sequence

def copy_file(
    src: str,
    dst: str,
    preserve_mode: bool = ...,
    preserve_times: bool = ...,
    update: bool = ...,
    link: str | None = None,
    verbose: bool = ...,
    dry_run: bool = ...,
) -> tuple[str, str]: ...
def move_file(src: str, dst: str, verbose: bool = ..., dry_run: bool = ...) -> str: ...
def write_file(filename: str, contents: Sequence[str]) -> None: ...
