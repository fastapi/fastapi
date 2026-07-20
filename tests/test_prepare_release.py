from datetime import date
from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts.prepare_release import (
    RELEASE_NOTES_HEADER,
    BumpType,
    app,
    bump_version,
    get_release_notes_body,
    update_release_notes,
    update_version_file,
)

runner = CliRunner()


def release_notes_content(body: str) -> str:
    return f"{RELEASE_NOTES_HEADER}{body}"


@pytest.mark.parametrize(
    ("current_version", "bump", "new_version"),
    [
        ("0.136.3", "major", "1.0.0"),
        ("0.136.3", "minor", "0.137.0"),
        ("0.136.3", "patch", "0.136.4"),
    ],
)
def test_bump_version(current_version: str, bump: BumpType, new_version: str) -> None:
    assert bump_version(current_version, bump) == new_version


def test_update_version_file() -> None:
    content = (
        '"""FastAPI framework, high performance, easy to learn, fast to code, '
        'ready for production"""\n\n__version__ = "0.136.3"\n'
    )

    new_content = update_version_file(content, "0.136.4", Path("fastapi/__init__.py"))

    assert new_content == (
        '"""FastAPI framework, high performance, easy to learn, fast to code, '
        'ready for production"""\n\n__version__ = "0.136.4"\n'
    )


def test_update_version_file_requires_newer_version() -> None:
    content = '__version__ = "0.136.3"\n'

    with pytest.raises(RuntimeError, match="must be greater"):
        update_version_file(content, "0.136.3", Path("fastapi/__init__.py"))


def test_update_release_notes() -> None:
    content = release_notes_content(
        """## Latest Changes

### Fixes

* Fix something.

## 0.136.3 (2026-05-23)

### Fixes

* Previous fix.
"""
    )

    new_content = update_release_notes(
        content, "0.136.4", date(2026, 5, 30), Path("docs/en/docs/release-notes.md")
    )

    assert new_content == release_notes_content(
        """## Latest Changes

## 0.136.4 (2026-05-30)

### Fixes

* Fix something.

## 0.136.3 (2026-05-23)

### Fixes

* Previous fix.
"""
    )


def test_update_release_notes_rejects_existing_version() -> None:
    content = release_notes_content(
        """## Latest Changes

## 0.136.4 (2026-05-30)
"""
    )

    with pytest.raises(RuntimeError, match="already contain"):
        update_release_notes(
            content, "0.136.4", date(2026, 5, 30), Path("docs/en/docs/release-notes.md")
        )


def test_get_release_notes_body_with_dated_heading() -> None:
    content = release_notes_content(
        """## Latest Changes

## 0.136.4 (2026-05-30)

### Fixes

* Fix something.

## 0.136.3 (2026-05-23)

### Fixes

* Previous fix.
"""
    )

    body = get_release_notes_body(
        content, "0.136.4", Path("docs/en/docs/release-notes.md")
    )

    assert body == "### Fixes\n\n* Fix something.\n"


def test_get_release_notes_body_with_plain_heading() -> None:
    content = release_notes_content(
        """## Latest Changes

## 0.136.4

### Fixes

* Fix something.
"""
    )

    body = get_release_notes_body(
        content, "0.136.4", Path("docs/en/docs/release-notes.md")
    )

    assert body == "### Fixes\n\n* Fix something.\n"


def test_get_release_notes_body_allows_non_version_h2_content() -> None:
    content = release_notes_content(
        """## Latest Changes

## 0.136.4

## Highlights

* Fix something.

## 0.136.3

* Previous fix.
"""
    )

    body = get_release_notes_body(
        content, "0.136.4", Path("docs/en/docs/release-notes.md")
    )

    assert body == "## Highlights\n\n* Fix something.\n"


def test_get_release_notes_body_requires_version_section() -> None:
    content = release_notes_content("## Latest Changes\n")

    with pytest.raises(RuntimeError, match="Could not find"):
        get_release_notes_body(
            content, "0.136.4", Path("docs/en/docs/release-notes.md")
        )


def test_get_release_notes_body_requires_non_empty_section() -> None:
    content = release_notes_content(
        """## Latest Changes

## 0.136.4

## 0.136.3

* Previous fix.
"""
    )

    with pytest.raises(RuntimeError, match="is empty"):
        get_release_notes_body(
            content, "0.136.4", Path("docs/en/docs/release-notes.md")
        )


def test_cli_updates_configured_files(tmp_path: Path) -> None:
    version_file = tmp_path / "fastapi" / "__init__.py"
    version_file.parent.mkdir()
    version_file.write_text('__version__ = "0.136.3"\n')
    release_notes_file = tmp_path / "release-notes.md"
    release_notes_file.write_text(
        release_notes_content(
            """## Latest Changes

### Fixes

* Fix something.
"""
        )
    )

    result = runner.invoke(
        app,
        [
            "prepare",
            "patch",
            "--version-file",
            str(version_file),
            "--release-notes-file",
            str(release_notes_file),
            "--date",
            "2026-05-30",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Prepared release 0.136.4 (2026-05-30)" in result.output
    assert version_file.read_text() == '__version__ = "0.136.4"\n'
    assert "## 0.136.4 (2026-05-30)" in release_notes_file.read_text()


def test_cli_accepts_env_vars(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    version_file = tmp_path / "fastapi" / "__init__.py"
    version_file.parent.mkdir()
    version_file.write_text('__version__ = "0.136.3"\n')
    release_notes_file = tmp_path / "docs" / "en" / "docs" / "release-notes.md"
    release_notes_file.parent.mkdir(parents=True)
    release_notes_file.write_text(release_notes_content("## Latest Changes\n"))
    monkeypatch.setenv("PREPARE_RELEASE_BUMP", "minor")
    monkeypatch.setenv("PREPARE_RELEASE_VERSION_FILE", str(version_file))
    monkeypatch.setenv("PREPARE_RELEASE_RELEASE_NOTES_FILE", str(release_notes_file))
    monkeypatch.setenv("PREPARE_RELEASE_DATE", "2026-05-30")

    result = runner.invoke(app, ["prepare"])

    assert result.exit_code == 0, result.output
    assert "Prepared release 0.137.0 (2026-05-30)" in result.output
    assert version_file.read_text() == '__version__ = "0.137.0"\n'
    assert "## 0.137.0 (2026-05-30)" in release_notes_file.read_text()


def test_cli_prints_current_version(tmp_path: Path) -> None:
    version_file = tmp_path / "fastapi" / "__init__.py"
    version_file.parent.mkdir()
    version_file.write_text('__version__ = "0.136.3"\n')

    result = runner.invoke(
        app,
        [
            "current-version",
            "--version-file",
            str(version_file),
        ],
    )

    assert result.exit_code == 0, result.output
    assert result.output == "0.136.3\n"


def test_cli_prints_release_notes(tmp_path: Path) -> None:
    version_file = tmp_path / "fastapi" / "__init__.py"
    version_file.parent.mkdir()
    version_file.write_text('__version__ = "0.136.4"\n')
    release_notes_file = tmp_path / "release-notes.md"
    release_notes_file.write_text(
        release_notes_content(
            """## Latest Changes

## 0.136.4 (2026-05-30)

### Fixes

* Fix something.
"""
        )
    )

    result = runner.invoke(
        app,
        [
            "release-notes",
            "--version-file",
            str(version_file),
            "--release-notes-file",
            str(release_notes_file),
        ],
    )

    assert result.exit_code == 0, result.output
    assert result.output == "### Fixes\n\n* Fix something.\n"
