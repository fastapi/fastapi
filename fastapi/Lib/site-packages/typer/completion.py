import os
import sys
from typing import Any, Dict, Tuple

import click

from ._compat_utils import _get_click_major
from ._completion_shared import Shells, get_completion_script, install
from .models import ParamMeta
from .params import Option
from .utils import get_params_from_function

try:
    import shellingham
except ImportError:  # pragma: nocover
    shellingham = None


_click_patched = False


def get_completion_inspect_parameters() -> Tuple[ParamMeta, ParamMeta]:
    completion_init()
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if shellingham and not test_disable_detection:
        parameters = get_params_from_function(_install_completion_placeholder_function)
    else:
        parameters = get_params_from_function(
            _install_completion_no_auto_placeholder_function
        )
    install_param, show_param = parameters.values()
    return install_param, show_param


def install_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma no cover
    if isinstance(value, str):
        shell, path = install(shell=value)
    else:
        shell, path = install()
    click.secho(f"{shell} completion installed in {path}", fg="green")
    click.echo("Completion will take effect once you restart the terminal")
    sys.exit(0)


def show_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma no cover
    prog_name = ctx.find_root().info_name
    assert prog_name
    complete_var = "_{}_COMPLETE".format(prog_name.replace("-", "_").upper())
    shell = ""
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if isinstance(value, str):
        shell = value
    elif shellingham and not test_disable_detection:
        shell, _ = shellingham.detect_shell()
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    click.echo(script_content)
    sys.exit(0)


# Create a fake command function to extract the completion parameters
def _install_completion_placeholder_function(
    install_completion: bool = Option(
        None,
        "--install-completion",
        is_flag=True,
        callback=install_callback,
        expose_value=False,
        help="Install completion for the current shell.",
    ),
    show_completion: bool = Option(
        None,
        "--show-completion",
        is_flag=True,
        callback=show_callback,
        expose_value=False,
        help="Show completion for the current shell, to copy it or customize the installation.",
    ),
) -> Any:
    pass  # pragma no cover


def _install_completion_no_auto_placeholder_function(
    install_completion: Shells = Option(
        None,
        callback=install_callback,
        expose_value=False,
        help="Install completion for the specified shell.",
    ),
    show_completion: Shells = Option(
        None,
        callback=show_callback,
        expose_value=False,
        help="Show completion for the specified shell, to copy it or customize the installation.",
    ),
) -> Any:
    pass  # pragma no cover


def completion_init() -> None:
    if _get_click_major() < 8:
        from ._completion_click7 import completion_init

        completion_init()
    else:
        from ._completion_click8 import completion_init

        completion_init()


# Re-implement Click's shell_complete to add error message with:
# Invalid completion instruction
# To use 7.x instruction style for compatibility
# And to add extra error messages, for compatibility with Typer in previous versions
# This is only called in new Command method, only used by Click 8.x+
def shell_complete(
    cli: click.BaseCommand,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: str,
    instruction: str,
) -> int:
    import click
    import click.shell_completion

    if "_" not in instruction:
        click.echo("Invalid completion instruction.", err=True)
        return 1

    # Click 8 changed the order/style of shell instructions from e.g.
    # source_bash to bash_source
    # Typer override to preserve the old style for compatibility
    # Original in Click 8.x commented:
    # shell, _, instruction = instruction.partition("_")
    instruction, _, shell = instruction.partition("_")
    # Typer override end

    comp_cls = click.shell_completion.get_completion_class(shell)

    if comp_cls is None:
        click.echo(f"Shell {shell} not supported.", err=True)
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    if instruction == "source":
        click.echo(comp.source())
        return 0

    if instruction == "complete":
        click.echo(comp.complete())
        return 0

    click.echo(f'Completion instruction "{instruction}" not supported.', err=True)
    return 1
