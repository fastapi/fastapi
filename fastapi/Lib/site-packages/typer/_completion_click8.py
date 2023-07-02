import os
import re
import sys
from typing import Any, Dict, List, Tuple

import click
import click.parser
import click.shell_completion

from ._completion_shared import (
    COMPLETION_SCRIPT_BASH,
    COMPLETION_SCRIPT_FISH,
    COMPLETION_SCRIPT_POWER_SHELL,
    COMPLETION_SCRIPT_ZSH,
    Shells,
)

try:
    import shellingham
except ImportError:  # pragma: nocover
    shellingham = None


class BashComplete(click.shell_completion.BashComplete):
    name = Shells.bash.value
    source_template = COMPLETION_SCRIPT_BASH

    def source_vars(self) -> Dict[str, Any]:
        return {
            "complete_func": self.func_name,
            "autocomplete_var": self.complete_var,
            "prog_name": self.prog_name,
        }

    def get_completion_args(self) -> Tuple[List[str], str]:
        cwords = click.parser.split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        return args, incomplete

    def format_completion(self, item: click.shell_completion.CompletionItem) -> str:
        # TODO: Explore replicating the new behavior from Click, with item types and
        # triggering completion for files and directories
        # return f"{item.type},{item.value}"
        return f"{item.value}"

    def complete(self) -> str:
        args, incomplete = self.get_completion_args()
        completions = self.get_completions(args, incomplete)
        out = [self.format_completion(item) for item in completions]
        return "\n".join(out)


class ZshComplete(click.shell_completion.ZshComplete):
    name = Shells.zsh.value
    source_template = COMPLETION_SCRIPT_ZSH

    def source_vars(self) -> Dict[str, Any]:
        return {
            "complete_func": self.func_name,
            "autocomplete_var": self.complete_var,
            "prog_name": self.prog_name,
        }

    def get_completion_args(self) -> Tuple[List[str], str]:
        completion_args = os.getenv("_TYPER_COMPLETE_ARGS", "")
        cwords = click.parser.split_arg_string(completion_args)
        args = cwords[1:]
        if args and not completion_args.endswith(" "):
            incomplete = args[-1]
            args = args[:-1]
        else:
            incomplete = ""
        return args, incomplete

    def format_completion(self, item: click.shell_completion.CompletionItem) -> str:
        def escape(s: str) -> str:
            return (
                s.replace('"', '""')
                .replace("'", "''")
                .replace("$", "\\$")
                .replace("`", "\\`")
            )

        # TODO: Explore replicating the new behavior from Click, pay attention to
        # the difference with and without escape
        # return f"{item.type}\n{item.value}\n{item.help if item.help else '_'}"
        if item.help:
            return f'"{escape(item.value)}":"{escape(item.help)}"'
        else:
            return f'"{escape(item.value)}"'

    def complete(self) -> str:
        args, incomplete = self.get_completion_args()
        completions = self.get_completions(args, incomplete)
        res = [self.format_completion(item) for item in completions]
        if res:
            args_str = "\n".join(res)
            return f"_arguments '*: :(({args_str}))'"
        else:
            return "_files"


class FishComplete(click.shell_completion.FishComplete):
    name = Shells.fish.value
    source_template = COMPLETION_SCRIPT_FISH

    def source_vars(self) -> Dict[str, Any]:
        return {
            "complete_func": self.func_name,
            "autocomplete_var": self.complete_var,
            "prog_name": self.prog_name,
        }

    def get_completion_args(self) -> Tuple[List[str], str]:
        completion_args = os.getenv("_TYPER_COMPLETE_ARGS", "")
        cwords = click.parser.split_arg_string(completion_args)
        args = cwords[1:]
        if args and not completion_args.endswith(" "):
            incomplete = args[-1]
            args = args[:-1]
        else:
            incomplete = ""
        return args, incomplete

    def format_completion(self, item: click.shell_completion.CompletionItem) -> str:
        # TODO: Explore replicating the new behavior from Click, pay attention to
        # the difference with and without formatted help
        # if item.help:
        #     return f"{item.type},{item.value}\t{item.help}"

        # return f"{item.type},{item.value}
        if item.help:
            formatted_help = re.sub(r"\s", " ", item.help)
            return f"{item.value}\t{formatted_help}"
        else:
            return f"{item.value}"

    def complete(self) -> str:
        complete_action = os.getenv("_TYPER_COMPLETE_FISH_ACTION", "")
        args, incomplete = self.get_completion_args()
        completions = self.get_completions(args, incomplete)
        show_args = [self.format_completion(item) for item in completions]
        if complete_action == "get-args":
            if show_args:
                return "\n".join(show_args)
        elif complete_action == "is-args":
            if show_args:
                # Activate complete args (no files)
                sys.exit(0)
            else:
                # Deactivate complete args (allow files)
                sys.exit(1)
        return ""  # pragma: no cover


class PowerShellComplete(click.shell_completion.ShellComplete):
    name = Shells.powershell.value
    source_template = COMPLETION_SCRIPT_POWER_SHELL

    def source_vars(self) -> Dict[str, Any]:
        return {
            "complete_func": self.func_name,
            "autocomplete_var": self.complete_var,
            "prog_name": self.prog_name,
        }

    def get_completion_args(self) -> Tuple[List[str], str]:
        completion_args = os.getenv("_TYPER_COMPLETE_ARGS", "")
        incomplete = os.getenv("_TYPER_COMPLETE_WORD_TO_COMPLETE", "")
        cwords = click.parser.split_arg_string(completion_args)
        args = cwords[1:]
        return args, incomplete

    def format_completion(self, item: click.shell_completion.CompletionItem) -> str:
        return f"{item.value}:::{item.help or ' '}"


def completion_init() -> None:
    click.shell_completion.add_completion_class(BashComplete, Shells.bash.value)
    click.shell_completion.add_completion_class(ZshComplete, Shells.zsh.value)
    click.shell_completion.add_completion_class(FishComplete, Shells.fish.value)
    click.shell_completion.add_completion_class(
        PowerShellComplete, Shells.powershell.value
    )
    click.shell_completion.add_completion_class(PowerShellComplete, Shells.pwsh.value)
