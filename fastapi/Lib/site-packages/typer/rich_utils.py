# Extracted and modified from https://github.com/ewels/rich-click

import inspect
import sys
from collections import defaultdict
from os import getenv
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Union

import click
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, RenderableType, group
from rich.emoji import Emoji
from rich.highlighter import RegexHighlighter
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

# Default styles
STYLE_OPTION = "bold cyan"
STYLE_SWITCH = "bold green"
STYLE_NEGATIVE_OPTION = "bold magenta"
STYLE_NEGATIVE_SWITCH = "bold red"
STYLE_METAVAR = "bold yellow"
STYLE_METAVAR_SEPARATOR = "dim"
STYLE_USAGE = "yellow"
STYLE_USAGE_COMMAND = "bold"
STYLE_DEPRECATED = "red"
STYLE_DEPRECATED_COMMAND = "dim"
STYLE_HELPTEXT_FIRST_LINE = ""
STYLE_HELPTEXT = "dim"
STYLE_OPTION_HELP = ""
STYLE_OPTION_DEFAULT = "dim"
STYLE_OPTION_ENVVAR = "dim yellow"
STYLE_REQUIRED_SHORT = "red"
STYLE_REQUIRED_LONG = "dim red"
STYLE_OPTIONS_PANEL_BORDER = "dim"
ALIGN_OPTIONS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_OPTIONS_TABLE_SHOW_LINES = False
STYLE_OPTIONS_TABLE_LEADING = 0
STYLE_OPTIONS_TABLE_PAD_EDGE = False
STYLE_OPTIONS_TABLE_PADDING = (0, 1)
STYLE_OPTIONS_TABLE_BOX = ""
STYLE_OPTIONS_TABLE_ROW_STYLES = None
STYLE_OPTIONS_TABLE_BORDER_STYLE = None
STYLE_COMMANDS_PANEL_BORDER = "dim"
ALIGN_COMMANDS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_COMMANDS_TABLE_SHOW_LINES = False
STYLE_COMMANDS_TABLE_LEADING = 0
STYLE_COMMANDS_TABLE_PAD_EDGE = False
STYLE_COMMANDS_TABLE_PADDING = (0, 1)
STYLE_COMMANDS_TABLE_BOX = ""
STYLE_COMMANDS_TABLE_ROW_STYLES = None
STYLE_COMMANDS_TABLE_BORDER_STYLE = None
STYLE_ERRORS_PANEL_BORDER = "red"
ALIGN_ERRORS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_ERRORS_SUGGESTION = "dim"
STYLE_ABORTED = "red"
_TERMINAL_WIDTH = getenv("TERMINAL_WIDTH")
MAX_WIDTH = int(_TERMINAL_WIDTH) if _TERMINAL_WIDTH else None
COLOR_SYSTEM: Optional[
    Literal["auto", "standard", "256", "truecolor", "windows"]
] = "auto"  # Set to None to disable colors
_TYPER_FORCE_DISABLE_TERMINAL = getenv("_TYPER_FORCE_DISABLE_TERMINAL")
FORCE_TERMINAL = (
    True
    if getenv("GITHUB_ACTIONS") or getenv("FORCE_COLOR") or getenv("PY_COLORS")
    else None
)
if _TYPER_FORCE_DISABLE_TERMINAL:
    FORCE_TERMINAL = False

# Fixed strings
DEPRECATED_STRING = "(deprecated) "
DEFAULT_STRING = "[default: {}]"
ENVVAR_STRING = "[env var: {}]"
REQUIRED_SHORT_STRING = "*"
REQUIRED_LONG_STRING = "[required]"
RANGE_STRING = " [{}]"
ARGUMENTS_PANEL_TITLE = "Arguments"
OPTIONS_PANEL_TITLE = "Options"
COMMANDS_PANEL_TITLE = "Commands"
ERRORS_PANEL_TITLE = "Error"
ABORTED_TEXT = "Aborted."

MARKUP_MODE_MARKDOWN = "markdown"
MARKUP_MODE_RICH = "rich"
_RICH_HELP_PANEL_NAME = "rich_help_panel"

MarkupMode = Literal["markdown", "rich", None]


# Rich regex highlighter
class OptionHighlighter(RegexHighlighter):
    """Highlights our special options."""

    highlights = [
        r"(^|\W)(?P<switch>\-\w+)(?![a-zA-Z0-9])",
        r"(^|\W)(?P<option>\-\-[\w\-]+)(?![a-zA-Z0-9])",
        r"(?P<metavar>\<[^\>]+\>)",
        r"(?P<usage>Usage: )",
    ]


class NegativeOptionHighlighter(RegexHighlighter):
    highlights = [
        r"(^|\W)(?P<negative_switch>\-\w+)(?![a-zA-Z0-9])",
        r"(^|\W)(?P<negative_option>\-\-[\w\-]+)(?![a-zA-Z0-9])",
    ]


highlighter = OptionHighlighter()
negative_highlighter = NegativeOptionHighlighter()


def _get_rich_console(stderr: bool = False) -> Console:
    return Console(
        theme=Theme(
            {
                "option": STYLE_OPTION,
                "switch": STYLE_SWITCH,
                "negative_option": STYLE_NEGATIVE_OPTION,
                "negative_switch": STYLE_NEGATIVE_SWITCH,
                "metavar": STYLE_METAVAR,
                "metavar_sep": STYLE_METAVAR_SEPARATOR,
                "usage": STYLE_USAGE,
            },
        ),
        highlighter=highlighter,
        color_system=COLOR_SYSTEM,
        force_terminal=FORCE_TERMINAL,
        width=MAX_WIDTH,
        stderr=stderr,
    )


def _make_rich_rext(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, return the text as a Rich Text with the request style.
    If `rich_markdown_enable` is `True`, also parse the text for Rich markup strings.
    If `rich_markup_enable` is `True`, parse as Markdown.

    Only one of `rich_markdown_enable` or `rich_markup_enable` can be True.
    If both are True, `rich_markdown_enable` takes precedence.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))


@group()
def _get_help_text(
    *,
    obj: Union[click.Command, click.Group],
    markup_mode: MarkupMode,
) -> Iterable[Union[Markdown, Text]]:
    """Build primary help text for a click command or group.

    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as deprecated, the deprecated string will be prepended.
    """
    # Prepend deprecated status
    if obj.deprecated:
        yield Text(DEPRECATED_STRING, style=STYLE_DEPRECATED)

    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help or "")

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_rext(
        text=first_line.strip(),
        style=STYLE_HELPTEXT_FIRST_LINE,
        markup_mode=markup_mode,
    )

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if remaining_paragraphs:
        if markup_mode != MARKUP_MODE_RICH:
            # Remove single linebreaks
            remaining_paragraphs = [
                x.replace("\n", " ").strip()
                if not x.startswith("\b")
                else "{}\n".format(x.strip("\b\n"))
                for x in remaining_paragraphs
            ]
            # Join back together
            remaining_lines = "\n".join(remaining_paragraphs)
        else:
            # Join with double linebreaks if markdown
            remaining_lines = "\n\n".join(remaining_paragraphs)

        yield _make_rich_rext(
            text=remaining_lines,
            style=STYLE_HELPTEXT,
            markup_mode=markup_mode,
        )


def _get_parameter_help(
    *,
    param: Union[click.Option, click.Argument, click.Parameter],
    ctx: click.Context,
    markup_mode: MarkupMode,
) -> Columns:
    """Build primary help text for a click option or argument.

    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if
    applicable.
    """
    # import here to avoid cyclic imports
    from .core import TyperArgument, TyperOption

    items: List[Union[Text, Markdown]] = []

    # Get the environment variable first

    envvar = getattr(param, "envvar", None)
    var_str = ""
    # https://github.com/pallets/click/blob/0aec1168ac591e159baf6f61026d6ae322c53aaf/src/click/core.py#L2720-L2726
    if envvar is None:
        if (
            getattr(param, "allow_from_autoenv", None)
            and getattr(ctx, "auto_envvar_prefix", None) is not None
            and param.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{param.name.upper()}"
    if envvar is not None:
        var_str = (
            envvar if isinstance(envvar, str) else ", ".join(str(d) for d in envvar)
        )

    # Main help text
    help_value: Union[str, None] = getattr(param, "help", None)
    if help_value:
        paragraphs = help_value.split("\n\n")
        # Remove single linebreaks
        if markup_mode != MARKUP_MODE_MARKDOWN:
            paragraphs = [
                x.replace("\n", " ").strip()
                if not x.startswith("\b")
                else "{}\n".format(x.strip("\b\n"))
                for x in paragraphs
            ]
        items.append(
            _make_rich_rext(
                text="\n".join(paragraphs).strip(),
                style=STYLE_OPTION_HELP,
                markup_mode=markup_mode,
            )
        )

    # Environment variable AFTER help text
    if envvar and getattr(param, "show_envvar", None):
        items.append(Text(ENVVAR_STRING.format(var_str), style=STYLE_OPTION_ENVVAR))

    # Default value
    # This uses Typer's specific param._get_default_string
    if isinstance(param, (TyperOption, TyperArgument)):
        if param.show_default:
            show_default_is_str = isinstance(param.show_default, str)
            default_value = param._extract_default_help_str(ctx=ctx)
            default_str = param._get_default_string(
                ctx=ctx,
                show_default_is_str=show_default_is_str,
                default_value=default_value,
            )
            if default_str:
                items.append(
                    Text(
                        DEFAULT_STRING.format(default_str),
                        style=STYLE_OPTION_DEFAULT,
                    )
                )

    # Required?
    if param.required:
        items.append(Text(REQUIRED_LONG_STRING, style=STYLE_REQUIRED_LONG))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_rext(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )


def _print_options_panel(
    *,
    name: str,
    params: Union[List[click.Option], List[click.Argument]],
    ctx: click.Context,
    markup_mode: MarkupMode,
    console: Console,
) -> None:
    options_rows: List[List[RenderableType]] = []
    required_rows: List[Union[str, Text]] = []
    for param in params:
        # Short and long form
        opt_long_strs = []
        opt_short_strs = []
        secondary_opt_long_strs = []
        secondary_opt_short_strs = []
        for opt_str in param.opts:
            if "--" in opt_str:
                opt_long_strs.append(opt_str)
            else:
                opt_short_strs.append(opt_str)
        for opt_str in param.secondary_opts:
            if "--" in opt_str:
                secondary_opt_long_strs.append(opt_str)
            else:
                secondary_opt_short_strs.append(opt_str)

        # Column for a metavar, if we have one
        metavar = Text(style=STYLE_METAVAR, overflow="fold")
        metavar_str = param.make_metavar()

        # Do it ourselves if this is a positional argument
        if (
            isinstance(param, click.Argument)
            and param.name
            and metavar_str == param.name.upper()
        ):
            metavar_str = param.type.name.upper()

        # Skip booleans and choices (handled above)
        if metavar_str != "BOOLEAN":
            metavar.append(metavar_str)

        # Range - from
        # https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706  # noqa: E501
        try:
            # skip count with default range type
            if (
                isinstance(param.type, click.types._NumberRangeBase)
                and isinstance(param, click.Option)
                and not (param.count and param.type.min == 0 and param.type.max is None)
            ):
                range_str = param.type._describe_range()
                if range_str:
                    metavar.append(RANGE_STRING.format(range_str))
        except AttributeError:  # pragma: no cover
            # click.types._NumberRangeBase is only in Click 8x onwards
            pass

        # Required asterisk
        required: Union[str, Text] = ""
        if param.required:
            required = Text(REQUIRED_SHORT_STRING, style=STYLE_REQUIRED_SHORT)

        # Highlighter to make [ | ] and <> dim
        class MetavarHighlighter(RegexHighlighter):
            highlights = [
                r"^(?P<metavar_sep>(\[|<))",
                r"(?P<metavar_sep>\|)",
                r"(?P<metavar_sep>(\]|>)$)",
            ]

        metavar_highlighter = MetavarHighlighter()

        required_rows.append(required)
        options_rows.append(
            [
                highlighter(",".join(opt_long_strs)),
                highlighter(",".join(opt_short_strs)),
                negative_highlighter(",".join(secondary_opt_long_strs)),
                negative_highlighter(",".join(secondary_opt_short_strs)),
                metavar_highlighter(metavar),
                _get_parameter_help(
                    param=param,
                    ctx=ctx,
                    markup_mode=markup_mode,
                ),
            ]
        )
    rows_with_required: List[List[RenderableType]] = []
    if any(required_rows):
        for required, row in zip(required_rows, options_rows):
            rows_with_required.append([required, *row])
    else:
        rows_with_required = options_rows
    if options_rows:
        t_styles: Dict[str, Any] = {
            "show_lines": STYLE_OPTIONS_TABLE_SHOW_LINES,
            "leading": STYLE_OPTIONS_TABLE_LEADING,
            "box": STYLE_OPTIONS_TABLE_BOX,
            "border_style": STYLE_OPTIONS_TABLE_BORDER_STYLE,
            "row_styles": STYLE_OPTIONS_TABLE_ROW_STYLES,
            "pad_edge": STYLE_OPTIONS_TABLE_PAD_EDGE,
            "padding": STYLE_OPTIONS_TABLE_PADDING,
        }
        box_style = getattr(box, t_styles.pop("box"), None)

        options_table = Table(
            highlight=True,
            show_header=False,
            expand=True,
            box=box_style,
            **t_styles,
        )
        for row in rows_with_required:
            options_table.add_row(*row)
        console.print(
            Panel(
                options_table,
                border_style=STYLE_OPTIONS_PANEL_BORDER,
                title=name,
                title_align=ALIGN_OPTIONS_PANEL,
            )
        )


def _print_commands_panel(
    *,
    name: str,
    commands: List[click.Command],
    markup_mode: MarkupMode,
    console: Console,
) -> None:
    t_styles: Dict[str, Any] = {
        "show_lines": STYLE_COMMANDS_TABLE_SHOW_LINES,
        "leading": STYLE_COMMANDS_TABLE_LEADING,
        "box": STYLE_COMMANDS_TABLE_BOX,
        "border_style": STYLE_COMMANDS_TABLE_BORDER_STYLE,
        "row_styles": STYLE_COMMANDS_TABLE_ROW_STYLES,
        "pad_edge": STYLE_COMMANDS_TABLE_PAD_EDGE,
        "padding": STYLE_COMMANDS_TABLE_PADDING,
    }
    box_style = getattr(box, t_styles.pop("box"), None)

    commands_table = Table(
        highlight=False,
        show_header=False,
        expand=True,
        box=box_style,
        **t_styles,
    )
    # Define formatting in first column, as commands don't match highlighter
    # regex
    commands_table.add_column(style="bold cyan", no_wrap=True)
    rows: List[List[Union[RenderableType, None]]] = []
    deprecated_rows: List[Union[RenderableType, None]] = []
    for command in commands:
        helptext = command.short_help or command.help or ""
        command_name = command.name or ""
        if command.deprecated:
            command_name_text = Text(f"{command_name}", style=STYLE_DEPRECATED_COMMAND)
            deprecated_rows.append(Text(DEPRECATED_STRING, style=STYLE_DEPRECATED))
        else:
            command_name_text = Text(command_name)
            deprecated_rows.append(None)
        rows.append(
            [
                command_name_text,
                _make_command_help(
                    help_text=helptext,
                    markup_mode=markup_mode,
                ),
            ]
        )
    rows_with_deprecated = rows
    if any(deprecated_rows):
        rows_with_deprecated = []
        for row, deprecated_text in zip(rows, deprecated_rows):
            rows_with_deprecated.append([*row, deprecated_text])
    for row in rows_with_deprecated:
        commands_table.add_row(*row)
    if commands_table.row_count:
        console.print(
            Panel(
                commands_table,
                border_style=STYLE_COMMANDS_PANEL_BORDER,
                title=name,
                title_align=ALIGN_COMMANDS_PANEL,
            )
        )


def rich_format_help(
    *,
    obj: Union[click.Command, click.Group],
    ctx: click.Context,
    markup_mode: MarkupMode,
) -> None:
    """Print nicely formatted help text using rich.

    Based on original code from rich-cli, by @willmcgugan.
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236

    Replacement for the click function format_help().
    Takes a command or group and builds the help text output.
    """
    console = _get_rich_console()

    # Print usage
    console.print(
        Padding(highlighter(obj.get_usage(ctx)), 1), style=STYLE_USAGE_COMMAND
    )

    # Print command / group help if we have some
    if obj.help:
        # Print with some padding
        console.print(
            Padding(
                Align(
                    _get_help_text(
                        obj=obj,
                        markup_mode=markup_mode,
                    ),
                    pad=False,
                ),
                (0, 1, 1, 1),
            )
        )
    panel_to_arguments: DefaultDict[str, List[click.Argument]] = defaultdict(list)
    panel_to_options: DefaultDict[str, List[click.Option]] = defaultdict(list)
    for param in obj.get_params(ctx):
        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue
        if isinstance(param, click.Argument):
            panel_name = (
                getattr(param, _RICH_HELP_PANEL_NAME, None) or ARGUMENTS_PANEL_TITLE
            )
            panel_to_arguments[panel_name].append(param)
        elif isinstance(param, click.Option):
            panel_name = (
                getattr(param, _RICH_HELP_PANEL_NAME, None) or OPTIONS_PANEL_TITLE
            )
            panel_to_options[panel_name].append(param)
    default_arguments = panel_to_arguments.get(ARGUMENTS_PANEL_TITLE, [])
    _print_options_panel(
        name=ARGUMENTS_PANEL_TITLE,
        params=default_arguments,
        ctx=ctx,
        markup_mode=markup_mode,
        console=console,
    )
    for panel_name, arguments in panel_to_arguments.items():
        if panel_name == ARGUMENTS_PANEL_TITLE:
            # Already printed above
            continue
        _print_options_panel(
            name=panel_name,
            params=arguments,
            ctx=ctx,
            markup_mode=markup_mode,
            console=console,
        )
    default_options = panel_to_options.get(OPTIONS_PANEL_TITLE, [])
    _print_options_panel(
        name=OPTIONS_PANEL_TITLE,
        params=default_options,
        ctx=ctx,
        markup_mode=markup_mode,
        console=console,
    )
    for panel_name, options in panel_to_options.items():
        if panel_name == OPTIONS_PANEL_TITLE:
            # Already printed above
            continue
        _print_options_panel(
            name=panel_name,
            params=options,
            ctx=ctx,
            markup_mode=markup_mode,
            console=console,
        )

    if isinstance(obj, click.MultiCommand):
        panel_to_commands: DefaultDict[str, List[click.Command]] = defaultdict(list)
        for command_name in obj.list_commands(ctx):
            command = obj.get_command(ctx, command_name)
            if command and not command.hidden:
                panel_name = (
                    getattr(command, _RICH_HELP_PANEL_NAME, None)
                    or COMMANDS_PANEL_TITLE
                )
                panel_to_commands[panel_name].append(command)

        # Print each command group panel
        default_commands = panel_to_commands.get(COMMANDS_PANEL_TITLE, [])
        _print_commands_panel(
            name=COMMANDS_PANEL_TITLE,
            commands=default_commands,
            markup_mode=markup_mode,
            console=console,
        )
        for panel_name, commands in panel_to_commands.items():
            if panel_name == COMMANDS_PANEL_TITLE:
                # Already printed above
                continue
            _print_commands_panel(
                name=panel_name,
                commands=commands,
                markup_mode=markup_mode,
                console=console,
            )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        epilogue_text = _make_rich_rext(text=epilogue, markup_mode=markup_mode)
        console.print(Padding(Align(epilogue_text, pad=False), 1))


def rich_format_error(self: click.ClickException) -> None:
    """Print richly formatted click errors.

    Called by custom exception handler to print richly formatted click errors.
    Mimics original click.ClickException.echo() function but with rich formatting.
    """
    console = _get_rich_console(stderr=True)
    ctx: Union[click.Context, None] = getattr(self, "ctx", None)
    if ctx is not None:
        console.print(ctx.get_usage())

    if ctx is not None and ctx.command.get_help_option(ctx) is not None:
        console.print(
            f"Try [blue]'{ctx.command_path} {ctx.help_option_names[0]}'[/] for help.",
            style=STYLE_ERRORS_SUGGESTION,
        )

    console.print(
        Panel(
            highlighter(self.format_message()),
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title=ERRORS_PANEL_TITLE,
            title_align=ALIGN_ERRORS_PANEL,
        )
    )


def rich_abort_error() -> None:
    """Print richly formatted abort error."""
    console = _get_rich_console(stderr=True)
    console.print(ABORTED_TEXT, style=STYLE_ABORTED)
