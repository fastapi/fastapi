from __future__ import annotations

from typing import Sequence

from pre_commit import lang_base
from pre_commit.prefix import Prefix

ENVIRONMENT_DIR = None
get_default_version = lang_base.basic_get_default_version
health_check = lang_base.basic_health_check
install_environment = lang_base.no_install
in_env = lang_base.no_env


def run_hook(
    prefix: Prefix,
    entry: str,
    args: Sequence[str],
    file_args: Sequence[str],
    *,
    is_local: bool,
    require_serial: bool,
    color: bool,
) -> tuple[int, bytes]:
    cmd = lang_base.hook_cmd(entry, args)
    cmd = (prefix.path(cmd[0]), *cmd[1:])
    return lang_base.run_xargs(
        cmd,
        file_args,
        require_serial=require_serial,
        color=color,
    )
