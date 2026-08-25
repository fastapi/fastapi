import logging
import secrets
import subprocess
from pathlib import Path

import yaml
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_repository: str
    github_token: SecretStr


class Repo(BaseModel):
    name: str
    html_url: str
    stars: int
    owner_login: str
    owner_html_url: str


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()

    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(settings.github_token.get_secret_value(), per_page=100)
    r = g.get_repo(settings.github_repository)
    repos = g.search_repositories(query="topic:fastapi")
    repos_list = list(repos)
    final_repos: list[Repo] = []
    for repo in repos_list[:100]:
        if repo.full_name == settings.github_repository:
            continue
        final_repos.append(
            Repo(
                name=repo.name,
                html_url=repo.html_url,
                stars=repo.stargazers_count,
                owner_login=repo.owner.login,
                owner_html_url=repo.owner.html_url,
            )
        )
    data = {"repos": [repo.model_dump() for repo in final_repos]}

    # Local development
    # repos_path = Path("../docs/en/data/topic_repos.yml")
    repos_path = Path("./docs/en/data/topic_repos.yml")
    repos_old_content = repos_path.read_text(encoding="utf-8")
    new_repos_content = yaml.dump(data, sort_keys=False, width=200, allow_unicode=True)
    if repos_old_content == new_repos_content:
        logging.info("The data hasn't changed. Finishing.")
        return
    repos_path.write_text(new_repos_content, encoding="utf-8")
    # Securely run git commands with validations to avoid injection and unsafe paths
    import re
    import shutil

    def _safe_branch_name(name: str) -> bool:
        return re.match(r"^[A-Za-z0-9._\-/]+$", name) is not None

    def _is_path_within_repo(path_str: str) -> bool:
        p = Path(path_str)
        repo_root = Path().resolve()
        target = p.resolve() if p.is_absolute() else (repo_root / p).resolve()
        return str(target).startswith(str(repo_root))

    def safe_run(cmd: list):
        if not isinstance(cmd, (list, tuple)) or len(cmd) < 2:
            raise ValueError("Invalid command")
        if cmd[0] != "git":
            raise ValueError("Only 'git' commands are allowed")
        subcmd = cmd[1]
        allowed = {"config", "checkout", "add", "commit", "push"}
        if subcmd not in allowed:
            raise ValueError(f"Disallowed git subcommand: {subcmd}")
        if subcmd == "checkout":
            if len(cmd) >= 4 and cmd[2] == "-b":
                branch = cmd[3]
                if not _safe_branch_name(branch):
                    raise ValueError("Unsafe branch name")
        elif subcmd == "add":
            if len(cmd) >= 3:
                path_arg = cmd[2]
                if not _is_path_within_repo(path_arg):
                    raise ValueError("Path outside repository")
        elif subcmd == "commit":
            if len(cmd) >= 4 and cmd[2] == "-m":
                msg = cmd[3]
                if "\n" in msg or "\r" in msg:
                    raise ValueError("Unsafe commit message")
        elif subcmd == "config":
            if len(cmd) >= 4:
                val = cmd[3]
                if "\n" in val or "\r" in val:
                    raise ValueError("Unsafe config value")
        git_path = shutil.which("git")
        if not git_path:
            raise RuntimeError("git not found in PATH")
        return subprocess.run(
            [git_path] + list(cmd[1:]),
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

    logging.info("Setting up GitHub Actions git user")
    safe_run(["git", "config", "user.name", "pr-submit[bot]"])
    safe_run(["git", "config", "user.email", "pr-submit[bot]@users.noreply.github.com"])
    branch_name = f"fastapi-topic-repos-{secrets.token_hex(4)}"
    logging.info(f"Creating a new branch {branch_name}")
    safe_run(["git", "checkout", "-b", branch_name])
    logging.info("Adding updated file")
    safe_run(["git", "add", str(repos_path)])
    logging.info("Committing updated file")
    message = "👥 Update FastAPI GitHub topic repositories"
    safe_run(["git", "commit", "-m", message])
    logging.info("Pushing branch")
    safe_run(["git", "push", "origin", branch_name])
    logging.info("Creating PR")
    pr = r.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")
    logging.info("Finished")


if __name__ == "__main__":
    main()
