import os
import re
import sys

import click
import click._bashcomplete

from ._completion_shared import get_completion_script

try:
    import shellingham
except ImportError:  # pragma: nocover
    shellingham = None


_click_patched = False


def do_bash_complete(cli: click.Command, prog_name: str) -> bool:
    cwords = click.parser.split_arg_string(os.getenv("COMP_WORDS", ""))
    cword = int(os.getenv("COMP_CWORD", 0))
    args = cwords[1:cword]
    try:
        incomplete = cwords[cword]
    except IndexError:
        incomplete = ""

    for item in click._bashcomplete.get_choices(cli, prog_name, args, incomplete):
        click.echo(item[0])
    return True


def do_zsh_complete(cli: click.Command, prog_name: str) -> bool:
    completion_args = os.getenv("_TYPER_COMPLETE_ARGS", "")
    cwords = click.parser.split_arg_string(completion_args)
    args = cwords[1:]
    if args and not completion_args.endswith(" "):
        incomplete = args[-1]
        args = args[:-1]
    else:
        incomplete = ""

    def escape(s: str) -> str:
        return (
            s.replace('"', '""')
            .replace("'", "''")
            .replace("$", "\\$")
            .replace("`", "\\`")
        )

    res = []
    for item, help in click._bashcomplete.get_choices(cli, prog_name, args, incomplete):
        if help:
            res.append(f'"{escape(item)}":"{escape(help)}"')
        else:
            res.append(f'"{escape(item)}"')
    if res:
        args_str = "\n".join(res)
        click.echo(f"_arguments '*: :(({args_str}))'")
    else:
        click.echo("_files")
    return True


def do_fish_complete(cli: click.Command, prog_name: str) -> bool:
    completion_args = os.getenv("_TYPER_COMPLETE_ARGS", "")
    complete_action = os.getenv("_TYPER_COMPLETE_FISH_ACTION", "")
    cwords = click.parser.split_arg_string(completion_args)
    args = cwords[1:]
    if args and not completion_args.endswith(" "):
        incomplete = args[-1]
        args = args[:-1]
    else:
        incomplete = ""
    show_args = []
    for item, help in click._bashcomplete.get_choices(cli, prog_name, args, incomplete):
        if help:
            formatted_help = re.sub(r"\s", " ", help)
            show_args.append(f"{item}\t{formatted_help}")
        else:
            show_args.append(item)
    if complete_action == "get-args":
        if show_args:
            for arg in show_args:
                click.echo(arg)
    elif complete_action == "is-args":
        if show_args:
            # Activate complete args (no files)
            sys.exit(0)
        else:
            # Deactivate complete args (allow files)
            sys.exit(1)
    return True


def do_powershell_complete(cli: click.Command, prog_name: str) -> bool:
    completion_args = os.getenv("_TYPER_COMPLETE_ARGS", "")
    incomplete = os.getenv("_TYPER_COMPLETE_WORD_TO_COMPLETE", "")
    cwords = click.parser.split_arg_string(completion_args)
    args = cwords[1:]
    for item, help in click._bashcomplete.get_choices(cli, prog_name, args, incomplete):
        click.echo(f"{item}:::{help or ' '}")

    return True


def do_shell_complete(*, cli: click.Command, prog_name: str, shell: str) -> bool:
    if shell == "bash":
        return do_bash_complete(cli, prog_name)
    elif shell == "zsh":
        return do_zsh_complete(cli, prog_name)
    elif shell == "fish":
        return do_fish_complete(cli, prog_name)
    elif shell in {"powershell", "pwsh"}:
        return do_powershell_complete(cli, prog_name)
    return False


def handle_shell_complete(
    cli: click.Command, prog_name: str, complete_var: str, complete_instr: str
) -> bool:
    if "_" not in complete_instr:
        click.echo("Invalid completion instruction.", err=True)
        sys.exit(1)
    command, shell = complete_instr.split("_", 1)
    if command == "source":
        click.echo(
            get_completion_script(
                prog_name=prog_name, complete_var=complete_var, shell=shell
            )
        )
        return True
    elif command == "complete":
        return do_shell_complete(cli=cli, prog_name=prog_name, shell=shell)
    click.echo(f'Completion instruction "{command}" not supported.', err=True)
    return False


def completion_init() -> None:
    global _click_patched
    if not _click_patched:
        testing = os.getenv("_TYPER_COMPLETE_TESTING")

        def testing_handle_shell_complete(
            cli: click.Command, prog_name: str, complete_var: str, complete_instr: str
        ) -> bool:
            result = handle_shell_complete(cli, prog_name, complete_var, complete_instr)
            if result:
                # Avoid fast_exit(1) in Click so Coverage can finish
                sys.exit(1)
            return result

        if testing:
            click._bashcomplete.bashcomplete = testing_handle_shell_complete
        else:
            click._bashcomplete.bashcomplete = handle_shell_complete
        _click_patched = True
