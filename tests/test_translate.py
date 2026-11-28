import importlib
import subprocess
import sys
import types
from pathlib import Path

import pytest
import typer

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


def test_translate_page_aborts_without_writing_after_max_failed_attempts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []

    class FakeResult:
        def __init__(self, output: str) -> None:
            self.output = output

    class FakeAgent:
        def __init__(self, model: str) -> None:
            self.model = model

        def run_sync(self, prompt: str) -> FakeResult:
            calls.append(prompt)
            return FakeResult("broken translation")

    def fail_validation(**kwargs: object) -> None:
        raise ValueError("validation error")

    class GitHubStubModule(types.ModuleType):
        Github = object

    class PydanticAIStubModule(types.ModuleType):
        Agent = FakeAgent

    git_stub = types.ModuleType("git")
    github_stub = GitHubStubModule("github")
    pydantic_ai_stub = PydanticAIStubModule("pydantic_ai")
    monkeypatch.setitem(sys.modules, "git", git_stub)
    monkeypatch.setitem(sys.modules, "github", github_stub)
    monkeypatch.setitem(sys.modules, "pydantic_ai", pydantic_ai_stub)
    monkeypatch.delitem(sys.modules, "scripts.translate", raising=False)
    translate = importlib.import_module("scripts.translate")
    monkeypatch.setattr(translate, "check_translation", fail_validation)

    (tmp_path / "docs/es").mkdir(parents=True)
    (tmp_path / "docs/en/docs").mkdir(parents=True)
    (tmp_path / "docs/language_names.yml").write_text("es: Spanish\n", encoding="utf-8")
    (tmp_path / "docs/es/llm-prompt.md").write_text(
        "Translate carefully.\n", encoding="utf-8"
    )
    en_doc = Path("docs/en/docs/index.md")
    (tmp_path / en_doc).write_text("# FastAPI\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    with pytest.raises(typer.Exit) as exc_info:
        translate.translate_page(language="es", en_path=en_doc)

    assert exc_info.value.exit_code == 1
    assert len(calls) == 3
    assert not (tmp_path / "docs/es/docs/index.md").exists()
