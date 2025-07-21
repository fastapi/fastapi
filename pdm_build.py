import os
from typing import Any, Dict

from pdm.backend.hooks import Context

TIANGOLO_BUILD_PACKAGE = os.getenv("TIANGOLO_BUILD_PACKAGE", "fastapi")


def pdm_build_initialize(context: Context) -> None:
    metadata = context.config.metadata
    # Get custom config for the current package, from the env var
    config: Dict[str, Any] = context.config.data["tool"]["tiangolo"][
        "_internal-slim-build"
    ]["packages"].get(TIANGOLO_BUILD_PACKAGE)
    if not config:
        return
    project_config: Dict[str, Any] = config["project"]
    # Override main [project] configs with custom configs for this package
    for key, value in project_config.items():
        metadata[key] = value
