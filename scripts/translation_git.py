import subprocess
from pathlib import Path


def has_translation_changes(repo_path: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "docs"],
        cwd=repo_path,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return bool(result.stdout)


def commit_translation_changes(
    *,
    repo_path: Path,
    bot_name: str,
    language: str | None,
    command: str | None,
) -> str | None:
    if not has_translation_changes(repo_path):
        print("No translation changes to commit")
        return None
    print("Setting up GitHub App git user")
    subprocess.run(["git", "config", "user.name", bot_name], cwd=repo_path, check=True)
    subprocess.run(
        [
            "git",
            "config",
            "user.email",
            f"{bot_name}@users.noreply.github.com",
        ],
        cwd=repo_path,
        check=True,
    )
    print("Adding updated files")
    subprocess.run(["git", "add", "docs"], cwd=repo_path, check=True)
    message = "🌐 Update translations"
    if language:
        message += f" for {language}"
    if command:
        message += f" ({command})"
    print("Committing updated files")
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)
    return message
