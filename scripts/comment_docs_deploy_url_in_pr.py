import logging
import sys
from typing import Union

from github import Github
from github.PullRequest import PullRequest
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_repository: str
    github_token: SecretStr
    deploy_url: str
    commit_sha: str


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    g = Github(settings.github_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    use_pr: Union[PullRequest, None] = None
    for pr in repo.get_pulls():
        if pr.head.sha == settings.commit_sha:
            use_pr = pr
            break
    if not use_pr:
        logging.error(f"No PR found for hash: {settings.commit_sha}")
        sys.exit(0)
    use_pr.as_issue().create_comment(
        f"📝 Docs preview for commit {settings.commit_sha} at: {settings.deploy_url}"
    )
    logging.info("Finished")
