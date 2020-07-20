import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import httpx
from github import Github
from github.NamedUser import NamedUser
from pydantic import BaseModel, BaseSettings, SecretStr

github_api = "https://api.github.com"
netlify_api = "https://api.netlify.com"


class Settings(BaseSettings):
    input_token: SecretStr
    github_repository: str
    github_event_path: Path
    github_event_name: Optional[str] = None


class Artifact(BaseModel):
    id: int
    node_id: str
    name: str
    size_in_bytes: int
    url: str
    archive_download_url: str
    expired: bool
    created_at: datetime
    updated_at: datetime


class ArtifactResponse(BaseModel):
    total_count: int
    artifacts: List[Artifact]


def get_message(commit: str) -> str:
    return f"Docs preview for commit {commit} at"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    g = Github(settings.input_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    owner: NamedUser = repo.owner
    headers = {"Authorization": f"token {settings.input_token.get_secret_value()}"}
    prs = list(repo.get_pulls(state="open"))
    for pr in prs:
        logging.info("-----")
        logging.info(f"Processing PR #{pr.number}: {pr.title}")
        pr_comments = list(pr.get_issue_comments())
        pr_commits = list(pr.get_commits())
        last_commit = pr_commits[0]
        for pr_commit in pr_commits:
            if pr_commit.commit.author.date > last_commit.commit.author.date:
                last_commit = pr_commit
        commit = last_commit.commit.sha
        logging.info(f"Last commit: {commit}")
        message = get_message(commit)
        notified = False
        for pr_comment in pr_comments:
            if message in pr_comment.body:
                notified = True
        logging.info(f"Docs preview was notified: {notified}")
        if not notified:
            response = httpx.get(
                f"{github_api}/repos/{settings.github_repository}/actions/artifacts",
                headers=headers,
            )
            data = response.json()
            artifacts_response = ArtifactResponse.parse_obj(data)
            use_artifact: Optional[Artifact] = None
            for artifact in artifacts_response.artifacts:
                if artifact.name == settings.input_name:
                    use_artifact = artifact
                    break
            if use_artifact:
                logging.info(f"Existing artifact: {use_artifact.name}")
                response = httpx.post(
                    "https://api.github.com/repos/tiangolo/fastapi/actions/workflows/preview-docs.yml/dispatches",
                    headers=headers,
                    json={
                        "ref": "master",
                        "inputs": {"pr": f"{pr.number}", "name": f"docs-zip-{commit}"},
                    },
                )
                logging.info(
                    f"Trigger sent, response status: {response.status_code} - content: {response.content}"
                )
    logging.info("Finished")
