from __future__ import annotations

from pre_commit import lang_base

ENVIRONMENT_DIR = None
get_default_version = lang_base.basic_get_default_version
health_check = lang_base.basic_health_check
install_environment = lang_base.no_install
in_env = lang_base.no_env
run_hook = lang_base.basic_run_hook
