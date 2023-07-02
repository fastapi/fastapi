from typing import Any

from ..cmd import Command

class bdist_rpm(Command):
    description: str
    user_options: Any
    boolean_options: Any
    negative_opt: Any
    bdist_base: Any
    rpm_base: Any
    dist_dir: Any
    python: Any
    fix_python: Any
    spec_only: Any
    binary_only: Any
    source_only: Any
    use_bzip2: Any
    distribution_name: Any
    group: Any
    release: Any
    serial: Any
    vendor: Any
    packager: Any
    doc_files: Any
    changelog: Any
    icon: Any
    prep_script: Any
    build_script: Any
    install_script: Any
    clean_script: Any
    verify_script: Any
    pre_install: Any
    post_install: Any
    pre_uninstall: Any
    post_uninstall: Any
    prep: Any
    provides: Any
    requires: Any
    conflicts: Any
    build_requires: Any
    obsoletes: Any
    keep_temp: int
    use_rpm_opt_flags: int
    rpm3_mode: int
    no_autoreq: int
    force_arch: Any
    quiet: int
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def finalize_package_data(self) -> None: ...
    def run(self) -> None: ...
