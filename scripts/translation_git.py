import subprocess
from pathlib import Path


def has_translation_changes(repo_path: Path) -> bool:
    import shutil

    if not isinstance(repo_path, Path):
        raise TypeError("repo_path must be a pathlib.Path")
    repo_path = repo_path.resolve()
    if not repo_path.is_dir() or not (repo_path / ".git").exists():
        return False

    git_path = shutil.which("git")
    if not git_path:
        raise FileNotFoundError("git executable not found in PATH")

    try:
        result = subprocess.run(
            [git_path, "status", "--porcelain", "--", "docs"],
            cwd=str(repo_path),
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError:
        return False
    return bool(result.stdout)


def commit_translation_changes(
    *,
    repo_path: Path,
    bot_name: str,
    language: str | None,
    command: str | None,
) -> str | None:
    import shutil

    if not isinstance(repo_path, Path):
        raise TypeError("repo_path must be a pathlib.Path")
    repo_path = repo_path.resolve()
    if not repo_path.is_dir() or not (repo_path / ".git").exists():
        print("No translation changes to commit")
        return None

    git_path = shutil.which("git")
    if not git_path:
        raise FileNotFoundError("git executable not found in PATH")

    if not has_translation_changes(repo_path):
        print("No translation changes to commit")
        return None

    # basic sanitization of inputs used as git config values
    if not isinstance(bot_name, str) or any(c in bot_name for c in "\n\r\x00"):
        raise ValueError("invalid bot_name")
    if language is not None and (not isinstance(language, str) or any(c in language for c in "\n\r\x00")):
        raise ValueError("invalid language")
    if command is not None and (not isinstance(command, str) or any(c in command for c in "\n\r\x00")):
        raise ValueError("invalid command")

    print("Setting up GitHub App git user")
    subprocess.run([git_path, "config", "user.name", bot_name], cwd=str(repo_path), check=True)
    subprocess.run(
        [
            git_path,
            "config",
            "user.email",
            f"{bot_name}@users.noreply.github.com",
        ],
        cwd=str(repo_path),
        check=True,
    )
    print("Adding updated files")
    subprocess.run([git_path, "add", "docs"], cwd=str(repo_path), check=True)
    message = "🌐 Update translations"
    if language:
        message += f" for {language}"
    if command:
        message += f" ({command})"
    print("Committing updated files")
    subprocess.run([git_path, "commit", "-m", message], cwd=str(repo_path), check=True)
    return message
