__all__ = ["version", "bootstrap"]

def version() -> str: ...
def bootstrap(
    *,
    root: str | None = None,
    upgrade: bool = False,
    user: bool = False,
    altinstall: bool = False,
    default_pip: bool = False,
    verbosity: int = 0,
) -> None: ...
