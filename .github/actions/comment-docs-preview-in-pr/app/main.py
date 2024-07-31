import logging
import sys
from typing import Union

import httpx
from github import Github
from github.PullRequest import PullRequest
from pydantic import SecretStr
from pydantic_settings import BaseSettings

github_api = "https://api.github.com"


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
    github_headers = {
        "Authorization": f"token {settings.input_token.get_secret_value()}"
    }
    url = f"{github_api}/repos/{settings.github_repository}/issues/{use_pr.number}/comments"
    logging.info(f"Using comments URL: {url}")
    response = httpx.post(
        url,
        headers=github_headers,
        json={
            "body": f"📝 Docs preview for commit {use_pr.head.sha} at: {settings.input_deploy_url}"
        },
    )
    if not (200 <= response.status_code <= 300):
        logging.error(f"Error posting comment: {response.text}")
        sys.exit(1)
    logging.info("Finished")
