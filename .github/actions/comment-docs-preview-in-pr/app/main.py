import logging
import sys
from pathlib import Path
from typing import Optional

import httpx
from github import Github
from github.PullRequest import PullRequest
from pydantic import BaseModel, BaseSettings, SecretStr, ValidationError

github_api = "https://api.github.com"


class Settings(BaseSettings):
    github_repository: str
    github_event_path: Path
    github_event_name: Optional[str] = None
    input_token: SecretStr
    input_deploy_url: str


class PartialGithubEventHeadCommit(BaseModel):
    id: str


class PartialGithubEventWorkflowRun(BaseModel):
    head_commit: PartialGithubEventHeadCommit


class PartialGithubEvent(BaseModel):
    workflow_run: PartialGithubEventWorkflowRun


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    g = Github(settings.input_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    try:
        event = PartialGithubEvent.parse_file(settings.github_event_path)
    except ValidationError as e:
        logging.error(f"Error parsing event file: {e.errors()}")
        sys.exit(0)
    use_pr: Optional[PullRequest] = None
    for pr in repo.get_pulls():
        if pr.head.sha == event.workflow_run.head_commit.id:
            use_pr = pr
            break
    if not use_pr:
        logging.error(f"No PR found for hash: {event.workflow_run.head_commit.id}")
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
