def mkpath(
    name: str, mode: int = 0o777, verbose: int = 1, dry_run: int = 0
) -> list[str]: ...
def create_tree(
    base_dir: str,
    files: list[str],
    mode: int = 0o777,
    verbose: int = 1,
    dry_run: int = 0,
) -> None: ...
def copy_tree(
    src: str,
    dst: str,
    preserve_mode: int = 1,
    preserve_times: int = 1,
    preserve_symlinks: int = 0,
    update: int = 0,
    verbose: int = 1,
    dry_run: int = 0,
) -> list[str]: ...
def remove_tree(directory: str, verbose: int = 1, dry_run: int = 0) -> None: ...
