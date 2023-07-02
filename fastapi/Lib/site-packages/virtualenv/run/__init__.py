from __future__ import annotations

import logging
import os
from functools import partial

from virtualenv.app_data import make_app_data
from virtualenv.config.cli.parser import VirtualEnvConfigParser
from virtualenv.report import LEVELS, setup_report
from virtualenv.run.session import Session
from virtualenv.seed.wheels.periodic_update import manual_upgrade
from virtualenv.version import __version__

from .plugin.activators import ActivationSelector
from .plugin.creators import CreatorSelector
from .plugin.discovery import get_discover
from .plugin.seeders import SeederSelector


def cli_run(args, options=None, setup_logging=True, env=None):  # noqa: FBT002
    """
    Create a virtual environment given some command line interface arguments.

    :param args: the command line arguments
    :param options: passing in a ``VirtualEnvOptions`` object allows return of the parsed options
    :param setup_logging: ``True`` if setup logging handlers, ``False`` to use handlers already registered
    :param env: environment variables to use
    :return: the session object of the creation (its structure for now is experimental and might change on short notice)
    """
    env = os.environ if env is None else env
    of_session = session_via_cli(args, options, setup_logging, env)
    with of_session:
        of_session.run()
    return of_session


def session_via_cli(args, options=None, setup_logging=True, env=None):  # noqa: FBT002
    """
    Create a virtualenv session (same as cli_run, but this does not perform the creation). Use this if you just want to
    query what the virtual environment would look like, but not actually create it.

    :param args: the command line arguments
    :param options: passing in a ``VirtualEnvOptions`` object allows return of the parsed options
    :param setup_logging: ``True`` if setup logging handlers, ``False`` to use handlers already registered
    :param env: environment variables to use
    :return: the session object of the creation (its structure for now is experimental and might change on short notice)
    """  # noqa: D205
    env = os.environ if env is None else env
    parser, elements = build_parser(args, options, setup_logging, env)
    options = parser.parse_args(args)
    creator, seeder, activators = tuple(
        e.create(options) for e in elements
    )  # create types
    return Session(
        options.verbosity,
        options.app_data,
        parser._interpreter,  # noqa: SLF001
        creator,
        seeder,
        activators,
    )


def build_parser(args=None, options=None, setup_logging=True, env=None):  # noqa: FBT002
    parser = VirtualEnvConfigParser(options, os.environ if env is None else env)
    add_version_flag(parser)
    parser.add_argument(
        "--with-traceback",
        dest="with_traceback",
        action="store_true",
        default=False,
        help="on failure also display the stacktrace internals of virtualenv",
    )
    _do_report_setup(parser, args, setup_logging)
    options = load_app_data(args, parser, options)
    handle_extra_commands(options)

    discover = get_discover(parser, args)
    parser._interpreter = interpreter = discover.interpreter  # noqa: SLF001
    if interpreter is None:
        msg = f"failed to find interpreter for {discover}"
        raise RuntimeError(msg)
    elements = [
        CreatorSelector(interpreter, parser),
        SeederSelector(interpreter, parser),
        ActivationSelector(interpreter, parser),
    ]
    options, _ = parser.parse_known_args(args)
    for element in elements:
        element.handle_selected_arg_parse(options)
    parser.enable_help()
    return parser, elements


def build_parser_only(args=None):
    """Used to provide a parser for the doc generation."""
    return build_parser(args)[0]


def handle_extra_commands(options):
    if options.upgrade_embed_wheels:
        result = manual_upgrade(options.app_data, options.env)
        raise SystemExit(result)


def load_app_data(args, parser, options):
    parser.add_argument(
        "--read-only-app-data",
        action="store_true",
        help="use app data folder in read-only mode (write operations will fail with error)",
    )
    options, _ = parser.parse_known_args(args, namespace=options)

    # here we need a write-able application data (e.g. the zipapp might need this for discovery cache)
    parser.add_argument(
        "--app-data",
        help="a data folder used as cache by the virtualenv",
        type=partial(
            make_app_data, read_only=options.read_only_app_data, env=options.env
        ),
        default=make_app_data(
            None, read_only=options.read_only_app_data, env=options.env
        ),
    )
    parser.add_argument(
        "--reset-app-data",
        action="store_true",
        help="start with empty app data folder",
    )
    parser.add_argument(
        "--upgrade-embed-wheels",
        action="store_true",
        help="trigger a manual update of the embedded wheels",
    )
    options, _ = parser.parse_known_args(args, namespace=options)
    if options.reset_app_data:
        options.app_data.reset()
    return options


def add_version_flag(parser):
    import virtualenv

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__} from {virtualenv.__file__}",
        help="display the version of the virtualenv package and its location, then exit",
    )


def _do_report_setup(parser, args, setup_logging):
    level_map = ", ".join(
        f"{logging.getLevelName(line)}={c}" for c, line in sorted(LEVELS.items())
    )
    msg = "verbosity = verbose - quiet, default {}, mapping => {}"
    verbosity_group = parser.add_argument_group(
        title="verbosity",
        description=msg.format(logging.getLevelName(LEVELS[3]), level_map),
    )
    verbosity = verbosity_group.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbose",
        help="increase verbosity",
        default=2,
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="count",
        dest="quiet",
        help="decrease verbosity",
        default=0,
    )
    option, _ = parser.parse_known_args(args)
    if setup_logging:
        setup_report(option.verbosity)


__all__ = [
    "cli_run",
    "session_via_cli",
]
