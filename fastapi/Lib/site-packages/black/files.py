import io
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    Union,
)

from mypy_extensions import mypyc_attr
from packaging.specifiers import InvalidSpecifier, Specifier, SpecifierSet
from packaging.version import InvalidVersion, Version
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

if sys.version_info >= (3, 11):
    try:
        import tomllib
    except ImportError:
        # Help users on older alphas
        if not TYPE_CHECKING:
            import tomli as tomllib
else:
    import tomli as tomllib

from black.handle_ipynb_magics import jupyter_dependencies_are_installed
from black.mode import TargetVersion
from black.output import err
from black.report import Report

if TYPE_CHECKING:
    import colorama  # noqa: F401


@lru_cache()
def find_project_root(
    srcs: Sequence[str], stdin_filename: Optional[str] = None
) -> Tuple[Path, str]:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.

    Returns a two-tuple with the first element as the project root path and
    the second element as a string describing the method by which the
    project root was discovered.
    """
    if stdin_filename is not None:
        srcs = tuple(stdin_filename if s == "-" else s for s in srcs)
    if not srcs:
        srcs = [str(Path.cwd().resolve())]

    path_srcs = [Path(Path.cwd(), src).resolve() for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory, ".git directory"

        if (directory / ".hg").is_dir():
            return directory, ".hg directory"

        if (directory / "pyproject.toml").is_file():
            return directory, "pyproject.toml"

    return directory, "file system root"


def find_pyproject_toml(path_search_start: Tuple[str, ...]) -> Optional[str]:
    """Find the absolute filepath to a pyproject.toml if it exists"""
    path_project_root, _ = find_project_root(path_search_start)
    path_pyproject_toml = path_project_root / "pyproject.toml"
    if path_pyproject_toml.is_file():
        return str(path_pyproject_toml)

    try:
        path_user_pyproject_toml = find_user_pyproject_toml()
        return (
            str(path_user_pyproject_toml)
            if path_user_pyproject_toml.is_file()
            else None
        )
    except (PermissionError, RuntimeError) as e:
        # We do not have access to the user-level config directory, so ignore it.
        err(f"Ignoring user configuration directory due to {e!r}")
        return None


@mypyc_attr(patchable=True)
def parse_pyproject_toml(path_config: str) -> Dict[str, Any]:
    """Parse a pyproject toml file, pulling out relevant parts for Black.

    If parsing fails, will raise a tomllib.TOMLDecodeError.
    """
    with open(path_config, "rb") as f:
        pyproject_toml = tomllib.load(f)
    config: Dict[str, Any] = pyproject_toml.get("tool", {}).get("black", {})
    config = {k.replace("--", "").replace("-", "_"): v for k, v in config.items()}

    if "target_version" not in config:
        inferred_target_version = infer_target_version(pyproject_toml)
        if inferred_target_version is not None:
            config["target_version"] = [v.name.lower() for v in inferred_target_version]

    return config


def infer_target_version(
    pyproject_toml: Dict[str, Any]
) -> Optional[List[TargetVersion]]:
    """Infer Black's target version from the project metadata in pyproject.toml.

    Supports the PyPA standard format (PEP 621):
    https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#requires-python

    If the target version cannot be inferred, returns None.
    """
    project_metadata = pyproject_toml.get("project", {})
    requires_python = project_metadata.get("requires-python", None)
    if requires_python is not None:
        try:
            return parse_req_python_version(requires_python)
        except InvalidVersion:
            pass
        try:
            return parse_req_python_specifier(requires_python)
        except (InvalidSpecifier, InvalidVersion):
            pass

    return None


def parse_req_python_version(requires_python: str) -> Optional[List[TargetVersion]]:
    """Parse a version string (i.e. ``"3.7"``) to a list of TargetVersion.

    If parsing fails, will raise a packaging.version.InvalidVersion error.
    If the parsed version cannot be mapped to a valid TargetVersion, returns None.
    """
    version = Version(requires_python)
    if version.release[0] != 3:
        return None
    try:
        return [TargetVersion(version.release[1])]
    except (IndexError, ValueError):
        return None


def parse_req_python_specifier(requires_python: str) -> Optional[List[TargetVersion]]:
    """Parse a specifier string (i.e. ``">=3.7,<3.10"``) to a list of TargetVersion.

    If parsing fails, will raise a packaging.specifiers.InvalidSpecifier error.
    If the parsed specifier cannot be mapped to a valid TargetVersion, returns None.
    """
    specifier_set = strip_specifier_set(SpecifierSet(requires_python))
    if not specifier_set:
        return None

    target_version_map = {f"3.{v.value}": v for v in TargetVersion}
    compatible_versions: List[str] = list(specifier_set.filter(target_version_map))
    if compatible_versions:
        return [target_version_map[v] for v in compatible_versions]
    return None


def strip_specifier_set(specifier_set: SpecifierSet) -> SpecifierSet:
    """Strip minor versions for some specifiers in the specifier set.

    For background on version specifiers, see PEP 440:
    https://peps.python.org/pep-0440/#version-specifiers
    """
    specifiers = []
    for s in specifier_set:
        if "*" in str(s):
            specifiers.append(s)
        elif s.operator in ["~=", "==", ">=", "==="]:
            version = Version(s.version)
            stripped = Specifier(f"{s.operator}{version.major}.{version.minor}")
            specifiers.append(stripped)
        elif s.operator == ">":
            version = Version(s.version)
            if len(version.release) > 2:
                s = Specifier(f">={version.major}.{version.minor}")
            specifiers.append(s)
        else:
            specifiers.append(s)

    return SpecifierSet(",".join(str(s) for s in specifiers))


@lru_cache()
def find_user_pyproject_toml() -> Path:
    r"""Return the path to the top-level user configuration for black.

    This looks for ~\.black on Windows and ~/.config/black on Linux and other
    Unix systems.

    May raise:
    - RuntimeError: if the current user has no homedir
    - PermissionError: if the current process cannot access the user's homedir
    """
    if sys.platform == "win32":
        # Windows
        user_config_path = Path.home() / ".black"
    else:
        config_root = os.environ.get("XDG_CONFIG_HOME", "~/.config")
        user_config_path = Path(config_root).expanduser() / "black"
    return user_config_path.resolve()


@lru_cache()
def get_gitignore(root: Path) -> PathSpec:
    """Return a PathSpec matching gitignore content if present."""
    gitignore = root / ".gitignore"
    lines: List[str] = []
    if gitignore.is_file():
        with gitignore.open(encoding="utf-8") as gf:
            lines = gf.readlines()
    try:
        return PathSpec.from_lines("gitwildmatch", lines)
    except GitWildMatchPatternError as e:
        err(f"Could not parse {gitignore}: {e}")
        raise


def normalize_path_maybe_ignore(
    path: Path,
    root: Path,
    report: Optional[Report] = None,
) -> Optional[str]:
    """Normalize `path`. May return `None` if `path` was ignored.

    `report` is where "path ignored" output goes.
    """
    try:
        abspath = path if path.is_absolute() else Path.cwd() / path
        normalized_path = abspath.resolve()
        try:
            root_relative_path = normalized_path.relative_to(root).as_posix()
        except ValueError:
            if report:
                report.path_ignored(
                    path, f"is a symbolic link that points outside {root}"
                )
            return None

    except OSError as e:
        if report:
            report.path_ignored(path, f"cannot be read because {e}")
        return None

    return root_relative_path


def path_is_ignored(
    path: Path, gitignore_dict: Dict[Path, PathSpec], report: Report
) -> bool:
    for gitignore_path, pattern in gitignore_dict.items():
        relative_path = normalize_path_maybe_ignore(path, gitignore_path, report)
        if relative_path is None:
            break
        if pattern.match_file(relative_path):
            report.path_ignored(path, "matches a .gitignore file content")
            return True
    return False


def path_is_excluded(
    normalized_path: str,
    pattern: Optional[Pattern[str]],
) -> bool:
    match = pattern.search(normalized_path) if pattern else None
    return bool(match and match.group(0))


def gen_python_files(
    paths: Iterable[Path],
    root: Path,
    include: Pattern[str],
    exclude: Pattern[str],
    extend_exclude: Optional[Pattern[str]],
    force_exclude: Optional[Pattern[str]],
    report: Report,
    gitignore_dict: Optional[Dict[Path, PathSpec]],
    *,
    verbose: bool,
    quiet: bool,
) -> Iterator[Path]:
    """Generate all files under `path` whose paths are not excluded by the
    `exclude_regex`, `extend_exclude`, or `force_exclude` regexes,
    but are included by the `include` regex.

    Symbolic links pointing outside of the `root` directory are ignored.

    `report` is where output about exclusions goes.
    """

    assert root.is_absolute(), f"INTERNAL ERROR: `root` must be absolute but is {root}"
    for child in paths:
        normalized_path = normalize_path_maybe_ignore(child, root, report)
        if normalized_path is None:
            continue

        # First ignore files matching .gitignore, if passed
        if gitignore_dict and path_is_ignored(child, gitignore_dict, report):
            continue

        # Then ignore with `--exclude` `--extend-exclude` and `--force-exclude` options.
        normalized_path = "/" + normalized_path
        if child.is_dir():
            normalized_path += "/"

        if path_is_excluded(normalized_path, exclude):
            report.path_ignored(child, "matches the --exclude regular expression")
            continue

        if path_is_excluded(normalized_path, extend_exclude):
            report.path_ignored(
                child, "matches the --extend-exclude regular expression"
            )
            continue

        if path_is_excluded(normalized_path, force_exclude):
            report.path_ignored(child, "matches the --force-exclude regular expression")
            continue

        if child.is_dir():
            # If gitignore is None, gitignore usage is disabled, while a Falsey
            # gitignore is when the directory doesn't have a .gitignore file.
            if gitignore_dict is not None:
                new_gitignore_dict = {
                    **gitignore_dict,
                    root / child: get_gitignore(child),
                }
            else:
                new_gitignore_dict = None
            yield from gen_python_files(
                child.iterdir(),
                root,
                include,
                exclude,
                extend_exclude,
                force_exclude,
                report,
                new_gitignore_dict,
                verbose=verbose,
                quiet=quiet,
            )

        elif child.is_file():
            if child.suffix == ".ipynb" and not jupyter_dependencies_are_installed(
                verbose=verbose, quiet=quiet
            ):
                continue
            include_match = include.search(normalized_path) if include else True
            if include_match:
                yield child


def wrap_stream_for_windows(
    f: io.TextIOWrapper,
) -> Union[io.TextIOWrapper, "colorama.AnsiToWin32"]:
    """
    Wrap stream with colorama's wrap_stream so colors are shown on Windows.

    If `colorama` is unavailable, the original stream is returned unmodified.
    Otherwise, the `wrap_stream()` function determines whether the stream needs
    to be wrapped for a Windows environment and will accordingly either return
    an `AnsiToWin32` wrapper or the original stream.
    """
    try:
        from colorama.initialise import wrap_stream
    except ImportError:
        return f
    else:
        # Set `strip=False` to avoid needing to modify test_express_diff_with_color.
        return wrap_stream(f, convert=None, strip=False, autoreset=False, wrap=True)
