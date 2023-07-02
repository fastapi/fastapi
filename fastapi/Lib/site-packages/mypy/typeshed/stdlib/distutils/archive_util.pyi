def make_archive(
    base_name: str,
    format: str,
    root_dir: str | None = None,
    base_dir: str | None = None,
    verbose: int = 0,
    dry_run: int = 0,
    owner: str | None = None,
    group: str | None = None,
) -> str: ...
def make_tarball(
    base_name: str,
    base_dir: str,
    compress: str | None = "gzip",
    verbose: int = 0,
    dry_run: int = 0,
    owner: str | None = None,
    group: str | None = None,
) -> str: ...
def make_zipfile(
    base_name: str, base_dir: str, verbose: int = 0, dry_run: int = 0
) -> str: ...
