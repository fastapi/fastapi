import subprocess
from pathlib import Path

import pytest

from scripts import translate
from scripts.translation_git import commit_translation_changes


def run_git(repo_path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_path,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def test_commit_translation_changes(tmp_path: Path) -> None:
    run_git(tmp_path, "init")
    run_git(tmp_path, "config", "user.name", "Test User")
    run_git(tmp_path, "config", "user.email", "test@example.com")
    run_git(tmp_path, "config", "commit.gpgsign", "false")
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    translation_path = docs_path / "translation.md"
    translation_path.write_text("Original\n")
    unrelated_path = tmp_path / "unrelated.txt"
    unrelated_path.write_text("Original\n")
    run_git(tmp_path, "add", ".")
    run_git(tmp_path, "commit", "-m", "Initial commit")
    translation_path.write_text("Translated\n")
    unrelated_path.write_text("Unrelated change\n")

    message = commit_translation_changes(
        repo_path=tmp_path,
        bot_name="pr-push[bot]",
        language="es",
        command="update-outdated",
    )

    assert message == "🌐 Update translations for es (update-outdated)"
    assert run_git(tmp_path, "log", "-1", "--format=%s") == message
    assert run_git(tmp_path, "log", "-1", "--format=%an") == "pr-push[bot]"
    assert (
        run_git(tmp_path, "log", "-1", "--format=%ae")
        == "pr-push[bot]@users.noreply.github.com"
    )
    assert (
        run_git(tmp_path, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD")
        == "docs/translation.md"
    )
    assert run_git(tmp_path, "diff", "--name-only") == "unrelated.txt"
    commit_sha = run_git(tmp_path, "rev-parse", "HEAD")

    result = commit_translation_changes(
        repo_path=tmp_path,
        bot_name="pr-push[bot]",
        language="es",
        command="update-outdated",
    )

    assert result is None
    assert run_git(tmp_path, "rev-parse", "HEAD") == commit_sha


def test_translate_lang_passes_target_language(monkeypatch: pytest.MonkeyPatch) -> None:
    en_path = Path("docs/en/docs/advanced/new-feature.md")
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(translate, "iter_en_paths_to_translate", lambda: [en_path])
    monkeypatch.setattr(
        translate,
        "translate_page",
        lambda **kwargs: calls.append(kwargs),
    )

    target_language = "pt"
    translate.translate_lang(language=target_language)

    assert len(calls) == 1
    assert calls[0]["language"] == target_language
    assert calls[0]["language"] != "es"
    assert calls[0]["en_path"] == en_path


def test_translate_lang_writes_to_target_language_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    en_path = Path("docs/en/docs/tutorial/new-tutorial.md")
    target_language = "de"

    monkeypatch.setattr(translate, "iter_en_paths_to_translate", lambda: [en_path])

    def mock_translate_page(*, language: str, en_path: Path) -> None:
        target_path = tmp_path / f"docs/{language}/docs/tutorial/new-tutorial.md"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("Mock translated content", encoding="utf-8")

    monkeypatch.setattr(translate, "translate_page", mock_translate_page)
    translate.translate_lang(language=target_language)

    expected_file = tmp_path / f"docs/{target_language}/docs/tutorial/new-tutorial.md"
    spanish_file = tmp_path / "docs/es/docs/tutorial/new-tutorial.md"

    assert expected_file.exists()
    assert expected_file.read_text(encoding="utf-8") == "Mock translated content"
    assert not spanish_file.exists()
