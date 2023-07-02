import inspect
import io
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

import click

from ._compat_utils import _get_click_major

if TYPE_CHECKING:  # pragma: no cover
    if _get_click_major() > 7:
        import click.shell_completion

    from .core import TyperCommand, TyperGroup
    from .main import Typer


NoneType = type(None)

AnyType = Type[Any]

Required = ...


class Context(click.Context):
    pass


class FileText(io.TextIOWrapper):
    pass


class FileTextWrite(FileText):
    pass


class FileBinaryRead(io.BufferedReader):
    pass


class FileBinaryWrite(io.BufferedWriter):
    pass


class CallbackParam(click.Parameter):
    pass


class DefaultPlaceholder:
    """
    You shouldn't use this class directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the new value is `None`.
    """

    def __init__(self, value: Any):
        self.value = value

    def __bool__(self) -> bool:
        return bool(self.value)


DefaultType = TypeVar("DefaultType")

CommandFunctionType = TypeVar("CommandFunctionType", bound=Callable[..., Any])


def Default(value: DefaultType) -> DefaultType:
    """
    You shouldn't use this function directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the new value is `None`.
    """
    return DefaultPlaceholder(value)  # type: ignore


class CommandInfo:
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type["TyperCommand"]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        callback: Optional[Callable[..., Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        # Rich settings
        rich_help_panel: Union[str, None] = None,
    ):
        self.name = name
        self.cls = cls
        self.context_settings = context_settings
        self.callback = callback
        self.help = help
        self.epilog = epilog
        self.short_help = short_help
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.no_args_is_help = no_args_is_help
        self.hidden = hidden
        self.deprecated = deprecated
        # Rich settings
        self.rich_help_panel = rich_help_panel


class TyperInfo:
    def __init__(
        self,
        typer_instance: Optional["Typer"] = Default(None),
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type["TyperGroup"]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        # Rich settings
        rich_help_panel: Union[str, None] = Default(None),
    ):
        self.typer_instance = typer_instance
        self.name = name
        self.cls = cls
        self.invoke_without_command = invoke_without_command
        self.no_args_is_help = no_args_is_help
        self.subcommand_metavar = subcommand_metavar
        self.chain = chain
        self.result_callback = result_callback
        self.context_settings = context_settings
        self.callback = callback
        self.help = help
        self.epilog = epilog
        self.short_help = short_help
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.hidden = hidden
        self.deprecated = deprecated
        self.rich_help_panel = rich_help_panel


class ParameterInfo:
    def __init__(
        self,
        *,
        default: Optional[Any] = None,
        param_decls: Optional[Sequence[str]] = None,
        callback: Optional[Callable[..., Any]] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        autocompletion: Optional[Callable[..., Any]] = None,
        # TyperArgument
        show_default: Union[bool, str] = True,
        show_choices: bool = True,
        show_envvar: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
        # Choice
        case_sensitive: bool = True,
        # Numbers
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        clamp: bool = False,
        # DateTime
        formats: Optional[List[str]] = None,
        # File
        mode: Optional[str] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = "strict",
        lazy: Optional[bool] = None,
        atomic: bool = False,
        # Path
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: Union[None, Type[str], Type[bytes]] = None,
        # Rich settings
        rich_help_panel: Union[str, None] = None,
    ):
        self.default = default
        self.param_decls = param_decls
        self.callback = callback
        self.metavar = metavar
        self.expose_value = expose_value
        self.is_eager = is_eager
        self.envvar = envvar
        self.shell_complete = shell_complete
        self.autocompletion = autocompletion
        # TyperArgument
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar
        self.help = help
        self.hidden = hidden
        # Choice
        self.case_sensitive = case_sensitive
        # Numbers
        self.min = min
        self.max = max
        self.clamp = clamp
        # DateTime
        self.formats = formats
        # File
        self.mode = mode
        self.encoding = encoding
        self.errors = errors
        self.lazy = lazy
        self.atomic = atomic
        # Path
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.writable = writable
        self.readable = readable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.path_type = path_type
        # Rich settings
        self.rich_help_panel = rich_help_panel


class OptionInfo(ParameterInfo):
    def __init__(
        self,
        *,
        # ParameterInfo
        default: Optional[Any] = None,
        param_decls: Optional[Sequence[str]] = None,
        callback: Optional[Callable[..., Any]] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        autocompletion: Optional[Callable[..., Any]] = None,
        # Option
        show_default: bool = True,
        prompt: Union[bool, str] = False,
        confirmation_prompt: bool = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: Optional[bool] = None,
        flag_value: Optional[Any] = None,
        count: bool = False,
        allow_from_autoenv: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = True,
        # Choice
        case_sensitive: bool = True,
        # Numbers
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        clamp: bool = False,
        # DateTime
        formats: Optional[List[str]] = None,
        # File
        mode: Optional[str] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = "strict",
        lazy: Optional[bool] = None,
        atomic: bool = False,
        # Path
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: Union[None, Type[str], Type[bytes]] = None,
        # Rich settings
        rich_help_panel: Union[str, None] = None,
    ):
        super().__init__(
            default=default,
            param_decls=param_decls,
            callback=callback,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
            autocompletion=autocompletion,
            # TyperArgument
            show_default=show_default,
            show_choices=show_choices,
            show_envvar=show_envvar,
            help=help,
            hidden=hidden,
            # Choice
            case_sensitive=case_sensitive,
            # Numbers
            min=min,
            max=max,
            clamp=clamp,
            # DateTime
            formats=formats,
            # File
            mode=mode,
            encoding=encoding,
            errors=errors,
            lazy=lazy,
            atomic=atomic,
            # Path
            exists=exists,
            file_okay=file_okay,
            dir_okay=dir_okay,
            writable=writable,
            readable=readable,
            resolve_path=resolve_path,
            allow_dash=allow_dash,
            path_type=path_type,
            # Rich settings
            rich_help_panel=rich_help_panel,
        )
        self.prompt = prompt
        self.confirmation_prompt = confirmation_prompt
        self.prompt_required = prompt_required
        self.hide_input = hide_input
        self.is_flag = is_flag
        self.flag_value = flag_value
        self.count = count
        self.allow_from_autoenv = allow_from_autoenv


class ArgumentInfo(ParameterInfo):
    def __init__(
        self,
        *,
        # ParameterInfo
        default: Optional[Any] = None,
        param_decls: Optional[Sequence[str]] = None,
        callback: Optional[Callable[..., Any]] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        autocompletion: Optional[Callable[..., Any]] = None,
        # TyperArgument
        show_default: Union[bool, str] = True,
        show_choices: bool = True,
        show_envvar: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
        # Choice
        case_sensitive: bool = True,
        # Numbers
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        clamp: bool = False,
        # DateTime
        formats: Optional[List[str]] = None,
        # File
        mode: Optional[str] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = "strict",
        lazy: Optional[bool] = None,
        atomic: bool = False,
        # Path
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: Union[None, Type[str], Type[bytes]] = None,
        # Rich settings
        rich_help_panel: Union[str, None] = None,
    ):
        super().__init__(
            default=default,
            param_decls=param_decls,
            callback=callback,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
            autocompletion=autocompletion,
            # TyperArgument
            show_default=show_default,
            show_choices=show_choices,
            show_envvar=show_envvar,
            help=help,
            hidden=hidden,
            # Choice
            case_sensitive=case_sensitive,
            # Numbers
            min=min,
            max=max,
            clamp=clamp,
            # DateTime
            formats=formats,
            # File
            mode=mode,
            encoding=encoding,
            errors=errors,
            lazy=lazy,
            atomic=atomic,
            # Path
            exists=exists,
            file_okay=file_okay,
            dir_okay=dir_okay,
            writable=writable,
            readable=readable,
            resolve_path=resolve_path,
            allow_dash=allow_dash,
            path_type=path_type,
            # Rich settings
            rich_help_panel=rich_help_panel,
        )


class ParamMeta:
    empty = inspect.Parameter.empty

    def __init__(
        self,
        *,
        name: str,
        default: Any = inspect.Parameter.empty,
        annotation: Any = inspect.Parameter.empty,
    ) -> None:
        self.name = name
        self.default = default
        self.annotation = annotation


class DeveloperExceptionConfig:
    def __init__(
        self,
        *,
        pretty_exceptions_enable: bool = True,
        pretty_exceptions_show_locals: bool = True,
        pretty_exceptions_short: bool = True,
    ) -> None:
        self.pretty_exceptions_enable = pretty_exceptions_enable
        self.pretty_exceptions_show_locals = pretty_exceptions_show_locals
        self.pretty_exceptions_short = pretty_exceptions_short
