from collections.abc import Callable

cli_main: Callable[[], None] | None = None
try:
    from fastapi_cli.cli import main as cli_main

except ImportError:  # pragma: no cover
    pass


def main() -> None:
    if cli_main is None:
        message = 'To use the fastapi command, please install "fastapi[standard]":\n\n\tpip install "fastapi[standard]"\n'
        print(message)
        raise RuntimeError(message)  # noqa: B904
    cli_main()
