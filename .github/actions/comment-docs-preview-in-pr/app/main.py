import logging
import sys
from typing import Union

from github import Github
from github.PullRequest import PullRequest
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_repository: str
    input_token: SecretStr
    input_deploy_url: str
    input_commit_sha: str


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    g = Github(settings.input_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    use_pr: Union[PullRequest, None] = None
    for pr in repo.get_pulls():
        if pr.head.sha == settings.input_commit_sha:
            use_pr = pr
            break
    if not use_pr:
        logging.error(f"No PR found for hash: {settings.input_commit_sha}")
        sys.exit(0)
    use_pr.as_issue().create_comment(
        f"📝 Docs preview for commit {settings.input_commit_sha} at: {settings.input_deploy_url}"
    )
    logging.info("Finished")
