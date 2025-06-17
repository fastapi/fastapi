import logging
import secrets
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

import httpx
import yaml
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

github_graphql_url = "https://api.github.com/graphql"


sponsors_query = """
query Q($after: String) {
  user(login: "tiangolo") {
    sponsorshipsAsMaintainer(first: 100, after: $after) {
      edges {
        cursor
        node {
          sponsorEntity {
            ... on Organization {
              login
              avatarUrl
              url
            }
            ... on User {
              login
              avatarUrl
              url
            }
          }
          tier {
            name
            monthlyPriceInDollars
          }
        }
      }
    }
  }
}
"""


class SponsorEntity(BaseModel):
    login: str
    avatarUrl: str
    url: str


class Tier(BaseModel):
    name: str
    monthlyPriceInDollars: float


class SponsorshipAsMaintainerNode(BaseModel):
    sponsorEntity: SponsorEntity
    tier: Tier


class SponsorshipAsMaintainerEdge(BaseModel):
    cursor: str
    node: SponsorshipAsMaintainerNode


class SponsorshipAsMaintainer(BaseModel):
    edges: list[SponsorshipAsMaintainerEdge]


class SponsorsUser(BaseModel):
    sponsorshipsAsMaintainer: SponsorshipAsMaintainer


class SponsorsResponseData(BaseModel):
    user: SponsorsUser


class SponsorsResponse(BaseModel):
    data: SponsorsResponseData


class Settings(BaseSettings):
    sponsors_token: SecretStr
    pr_token: SecretStr
    github_repository: str
    httpx_timeout: int = 30


def get_graphql_response(
    *,
    settings: Settings,
    query: str,
    after: str | None = None,
) -> dict[str, Any]:
    headers = {"Authorization": f"token {settings.sponsors_token.get_secret_value()}"}
    variables = {"after": after}
    response = httpx.post(
        github_graphql_url,
        headers=headers,
        timeout=settings.httpx_timeout,
        json={"query": query, "variables": variables, "operationName": "Q"},
    )
    if response.status_code != 200:
        logging.error(f"Response was not 200, after: {after}")
        logging.error(response.text)
        raise RuntimeError(response.text)
    data = response.json()
    if "errors" in data:
        logging.error(f"Errors in response, after: {after}")
        logging.error(data["errors"])
        logging.error(response.text)
        raise RuntimeError(response.text)
    return data


def get_graphql_sponsor_edges(
    *, settings: Settings, after: str | None = None
) -> list[SponsorshipAsMaintainerEdge]:
    data = get_graphql_response(settings=settings, query=sponsors_query, after=after)
    graphql_response = SponsorsResponse.model_validate(data)
    return graphql_response.data.user.sponsorshipsAsMaintainer.edges


def get_individual_sponsors(
    settings: Settings,
) -> defaultdict[float, dict[str, SponsorEntity]]:
    nodes: list[SponsorshipAsMaintainerNode] = []
    edges = get_graphql_sponsor_edges(settings=settings)

    while edges:
        for edge in edges:
            nodes.append(edge.node)
        last_edge = edges[-1]
        edges = get_graphql_sponsor_edges(settings=settings, after=last_edge.cursor)

    tiers: defaultdict[float, dict[str, SponsorEntity]] = defaultdict(dict)
    for node in nodes:
        tiers[node.tier.monthlyPriceInDollars][node.sponsorEntity.login] = (
            node.sponsorEntity
        )
    return tiers


def update_content(*, content_path: Path, new_content: Any) -> bool:
    old_content = content_path.read_text(encoding="utf-8")

    new_content = yaml.dump(new_content, sort_keys=False, width=200, allow_unicode=True)
    if old_content == new_content:
        logging.info(f"The content hasn't changed for {content_path}")
        return False
    content_path.write_text(new_content, encoding="utf-8")
    logging.info(f"Updated {content_path}")
    return True


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(settings.pr_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)

    tiers = get_individual_sponsors(settings=settings)
    keys = list(tiers.keys())
    keys.sort(reverse=True)
    sponsors = []
    for key in keys:
        sponsor_group = []
        for login, sponsor in tiers[key].items():
            sponsor_group.append(
                {"login": login, "avatarUrl": sponsor.avatarUrl, "url": sponsor.url}
            )
        sponsors.append(sponsor_group)
    github_sponsors = {
        "sponsors": sponsors,
    }

    # For local development
    # github_sponsors_path = Path("../docs/en/data/github_sponsors.yml")
    github_sponsors_path = Path("./docs/en/data/github_sponsors.yml")
    updated = update_content(
        content_path=github_sponsors_path, new_content=github_sponsors
    )

    if not updated:
        logging.info("The data hasn't changed, finishing.")
        return

    logging.info("Setting up GitHub Actions git user")
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions@github.com"], check=True
    )
    branch_name = f"fastapi-people-sponsors-{secrets.token_hex(4)}"
    logging.info(f"Creating a new branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    logging.info("Adding updated file")
    subprocess.run(
        [
            "git",
            "add",
            str(github_sponsors_path),
        ],
        check=True,
    )
    logging.info("Committing updated file")
    message = "👥 Update FastAPI People - Sponsors"
    subprocess.run(["git", "commit", "-m", message], check=True)
    logging.info("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    logging.info("Creating PR")
    pr = repo.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")
    logging.info("Finished")


if __name__ == "__main__":
    main()
