import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import httpx
from pydantic import BaseModel, BaseSettings, SecretStr

github_api = "https://api.github.com"
netlify_api = "https://api.netlify.com"


class Settings(BaseSettings):
    input_name: str
    input_token: SecretStr
    input_path: str
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    github_headers = {
        "Authorization": f"token {settings.input_token.get_secret_value()}"
    }
    response = httpx.get(
        f"{github_api}/repos/{settings.github_repository}/actions/artifacts",
        headers=github_headers,
    )
    data = response.json()
    artifacts_response = ArtifactResponse.parse_obj(data)
    use_artifact: Optional[Artifact] = None
    for artifact in artifacts_response.artifacts:
        if artifact.name == settings.input_name:
            use_artifact = artifact
            break
    assert use_artifact
    file_response = httpx.get(
        use_artifact.archive_download_url, headers=github_headers, timeout=30
    )
    zip_file = Path(settings.input_path)
    zip_file.write_bytes(file_response.content)
    logging.info("Finished")
