import os
from typing import Any

from pdm.backend.hooks import Context

TIANGOLO_BUILD_PACKAGE = os.getenv("TIANGOLO_BUILD_PACKAGE")


def pdm_build_initialize(context: Context) -> None:
    metadata = context.config.metadata
    # Get main version
    version = metadata["version"]
    # Get custom config for the current package, from the env var
    all_configs_config: dict[str, Any] = context.config.data["tool"]["tiangolo"][
        "_internal-slim-build"
    ]["packages"]

    if TIANGOLO_BUILD_PACKAGE not in all_configs_config:
        return

    config = all_configs_config[TIANGOLO_BUILD_PACKAGE]
    project_config: dict[str, Any] = config["project"]
    # Override main [project] configs with custom configs for this package
    for key, value in project_config.items():
        metadata[key] = value
    # Get custom build config for the current package
    build_config: dict[str, Any] = (
        config.get("tool", {}).get("pdm", {}).get("build", {})
    )
    # Override PDM build config with custom build config for this package
    for key, value in build_config.items():
        context.config.build_config[key] = value
    # Get main dependencies
    dependencies: list[str] = metadata.get("dependencies", [])
    # Sync versions in dependencies
    new_dependencies = []
    for dep in dependencies:
        new_dep = f"{dep}>={version}"
        new_dependencies.append(new_dep)
    metadata["dependencies"] = new_dependencies
