"""Prepare a release by updating the package version and release notes."""

import re
from datetime import date
from pathlib import Path
from typing import Annotated, Literal

import typer

VERSION_PATTERN = re.compile(r'(?m)^__version__ = "(\d+\.\d+\.\d+)"$')
VERSION_HEADING_PATTERN = re.compile(r"(?m)^## (\d+\.\d+\.\d+)(?: \([^)]+\))?$")
RELEASE_NOTES_HEADER = """---
hide:
  - navigation
---

# Release Notes

"""
LATEST_CHANGES_HEADER = "## Latest Changes"
BumpType = Literal["major", "minor", "patch"]

app = typer.Typer()


def parse_version(version: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"\d+\.\d+\.\d+", version)
    if not match:
        raise ValueError(f"Invalid version: {version!r}. Expected format: X.Y.Z")
    major, minor, patch = version.split(".")
    return int(major), int(minor), int(patch)


def get_current_version(content: str, version_file: Path) -> str:
    matches = list(VERSION_PATTERN.finditer(content))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one __version__ assignment in {version_file}, "
            f"found {len(matches)}"
        )
    return matches[0].group(1)


def bump_version(version: str, bump: BumpType) -> str:
    major, minor, patch = parse_version(version)
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def update_version_file(content: str, version: str, version_file: Path) -> str:
    current_version = get_current_version(content, version_file)
    if parse_version(version) <= parse_version(current_version):
        raise RuntimeError(
            f"New version {version} must be greater than current version {current_version}"
        )
    return VERSION_PATTERN.sub(f'__version__ = "{version}"', content, count=1)


def update_release_notes(
    content: str, version: str, release_date: date, release_notes_file: Path
) -> str:
    if not content.startswith(RELEASE_NOTES_HEADER):
        raise RuntimeError(
            f"{release_notes_file} must start with {RELEASE_NOTES_HEADER!r}"
        )
    if re.search(rf"^## {re.escape(version)}(?: \([^)]+\))?$", content, re.M):
        raise RuntimeError(f"Release notes already contain a section for {version}")

    latest_header = f"{RELEASE_NOTES_HEADER}{LATEST_CHANGES_HEADER}\n"
    if not content.startswith(latest_header):
        raise RuntimeError(f"{release_notes_file} must start with {latest_header!r}")

    release_header = f"## {version} ({release_date.isoformat()})"
    return content.replace(
        latest_header,
        f"{RELEASE_NOTES_HEADER}{LATEST_CHANGES_HEADER}\n\n{release_header}\n",
        1,
    )


def get_release_notes_body(content: str, version: str, release_notes_file: Path) -> str:
    version_heading = re.compile(rf"(?m)^## {re.escape(version)}(?: \([^)]+\))?$")
    match = version_heading.search(content)
    if not match:
        raise RuntimeError(
            f"Could not find release notes section for {version} in {release_notes_file}"
        )

    next_match = VERSION_HEADING_PATTERN.search(content, match.end())
    end = next_match.start() if next_match else len(content)
    body = content[match.end() : end].strip()
    if not body:
        raise RuntimeError(
            f"Release notes section for {version} in {release_notes_file} is empty"
        )
    return f"{body}\n"


@app.command()
def prepare(
    bump: Annotated[
        BumpType,
        typer.Argument(
            envvar="PREPARE_RELEASE_BUMP",
            help="The release bump to make: major, minor, or patch.",
        ),
    ],
    version_file: Annotated[
        Path,
        typer.Option(
            envvar="PREPARE_RELEASE_VERSION_FILE",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            writable=True,
            help="Path to the Python file containing the __version__ assignment.",
        ),
    ],
    release_notes_file: Annotated[
        Path,
        typer.Option(
            envvar="PREPARE_RELEASE_RELEASE_NOTES_FILE",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            writable=True,
            help="Path to the release notes Markdown file.",
        ),
    ],
    release_date: Annotated[
        str,
        typer.Option(
            "--date",
            envvar="PREPARE_RELEASE_DATE",
            help="Release date in YYYY-MM-DD format. Defaults to today.",
        ),
    ] = date.today().isoformat(),
) -> None:
    parsed_release_date = date.fromisoformat(release_date or date.today().isoformat())

    version_file_content = version_file.read_text()
    release_notes_content = release_notes_file.read_text()
    version = bump_version(
        get_current_version(version_file_content, version_file), bump
    )

    version_file.write_text(
        update_version_file(version_file_content, version, version_file)
    )
    release_notes_file.write_text(
        update_release_notes(
            release_notes_content, version, parsed_release_date, release_notes_file
        )
    )

    typer.echo(f"Prepared release {version} ({parsed_release_date.isoformat()})")


@app.command()
def current_version(
    version_file: Annotated[
        Path,
        typer.Option(
            envvar="PREPARE_RELEASE_VERSION_FILE",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to the Python file containing the __version__ assignment.",
        ),
    ],
) -> None:
    typer.echo(get_current_version(version_file.read_text(), version_file))


@app.command()
def release_notes(
    version_file: Annotated[
        Path,
        typer.Option(
            envvar="PREPARE_RELEASE_VERSION_FILE",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to the Python file containing the __version__ assignment.",
        ),
    ],
    release_notes_file: Annotated[
        Path,
        typer.Option(
            envvar="PREPARE_RELEASE_RELEASE_NOTES_FILE",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to the release notes Markdown file.",
        ),
    ],
) -> None:
    version = get_current_version(version_file.read_text(), version_file)
    typer.echo(
        get_release_notes_body(
            release_notes_file.read_text(), version, release_notes_file
        ),
        nl=False,
    )


if __name__ == "__main__":
    app()
