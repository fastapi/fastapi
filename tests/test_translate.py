import subprocess
from pathlib import Path

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
