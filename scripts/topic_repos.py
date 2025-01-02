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
    data = [repo.model_dump() for repo in final_repos]

    # Local development
    # repos_path = Path("../docs/en/data/topic_repos.yml")
    repos_path = Path("./docs/en/data/topic_repos.yml")
    repos_old_content = repos_path.read_text(encoding="utf-8")
    new_repos_content = yaml.dump(data, sort_keys=False, width=200, allow_unicode=True)
    if repos_old_content == new_repos_content:
        logging.info("The data hasn't changed. Finishing.")
        return
    repos_path.write_text(new_repos_content, encoding="utf-8")
    logging.info("Setting up GitHub Actions git user")
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions@github.com"], check=True
    )
    branch_name = f"fastapi-topic-repos-{secrets.token_hex(4)}"
    logging.info(f"Creating a new branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    logging.info("Adding updated file")
    subprocess.run(["git", "add", str(repos_path)], check=True)
    logging.info("Committing updated file")
    message = "👥 Update FastAPI GitHub topic repositories"
    subprocess.run(["git", "commit", "-m", message], check=True)
    logging.info("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    logging.info("Creating PR")
    pr = r.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")
    logging.info("Finished")


if __name__ == "__main__":
    main()
