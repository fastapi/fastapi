import logging
import secrets
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import yaml
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

github_graphql_url = "https://api.github.com/graphql"


prs_query = """
query Q($after: String) {
  repository(name: "fastapi", owner: "fastapi") {
    pullRequests(first: 100, after: $after) {
      edges {
        cursor
        node {
          number
          labels(first: 100) {
            nodes {
              name
            }
          }
          author {
            login
            avatarUrl
            url
          }
          title
          createdAt
          lastEditedAt
          updatedAt
          state
          reviews(first:100) {
            nodes {
              author {
                login
                avatarUrl
                url
              }
              state
            }
          }
        }
      }
    }
  }
}
"""


class Author(BaseModel):
    login: str
    avatarUrl: str
    url: str


class LabelNode(BaseModel):
    name: str


class Labels(BaseModel):
    nodes: list[LabelNode]


class ReviewNode(BaseModel):
    author: Author | None = None
    state: str


class Reviews(BaseModel):
    nodes: list[ReviewNode]


class PullRequestNode(BaseModel):
    number: int
    labels: Labels
    author: Author | None = None
    title: str
    createdAt: datetime
    lastEditedAt: datetime | None = None
    updatedAt: datetime | None = None
    state: str
    reviews: Reviews


class PullRequestEdge(BaseModel):
    cursor: str
    node: PullRequestNode


class PullRequests(BaseModel):
    edges: list[PullRequestEdge]


class PRsRepository(BaseModel):
    pullRequests: PullRequests


class PRsResponseData(BaseModel):
    repository: PRsRepository


class PRsResponse(BaseModel):
    data: PRsResponseData


class Settings(BaseSettings):
    github_token: SecretStr
    github_repository: str
    httpx_timeout: int = 30


def get_graphql_response(
    *,
    settings: Settings,
    query: str,
    after: str | None = None,
) -> dict[str, Any]:
    headers = {"Authorization": f"token {settings.github_token.get_secret_value()}"}
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


def get_graphql_pr_edges(
    *, settings: Settings, after: str | None = None
) -> list[PullRequestEdge]:
    data = get_graphql_response(settings=settings, query=prs_query, after=after)
    graphql_response = PRsResponse.model_validate(data)
    return graphql_response.data.repository.pullRequests.edges


def get_pr_nodes(settings: Settings) -> list[PullRequestNode]:
    pr_nodes: list[PullRequestNode] = []
    pr_edges = get_graphql_pr_edges(settings=settings)

    while pr_edges:
        for edge in pr_edges:
            pr_nodes.append(edge.node)
        last_edge = pr_edges[-1]
        pr_edges = get_graphql_pr_edges(settings=settings, after=last_edge.cursor)
    return pr_nodes


class ContributorsResults(BaseModel):
    contributors: Counter[str]
    translation_reviewers: Counter[str]
    translators: Counter[str]
    authors: dict[str, Author]


def get_contributors(pr_nodes: list[PullRequestNode]) -> ContributorsResults:
    contributors = Counter[str]()
    translation_reviewers = Counter[str]()
    translators = Counter[str]()
    authors: dict[str, Author] = {}

    for pr in pr_nodes:
        if pr.author:
            authors[pr.author.login] = pr.author
        is_lang = False
        for label in pr.labels.nodes:
            if label.name == "lang-all":
                is_lang = True
                break
        for review in pr.reviews.nodes:
            if review.author:
                authors[review.author.login] = review.author
                if is_lang:
                    translation_reviewers[review.author.login] += 1
        if pr.state == "MERGED" and pr.author:
            if is_lang:
                translators[pr.author.login] += 1
            else:
                contributors[pr.author.login] += 1
    return ContributorsResults(
        contributors=contributors,
        translation_reviewers=translation_reviewers,
        translators=translators,
        authors=authors,
    )


def get_users_to_write(
    *,
    counter: Counter[str],
    authors: dict[str, Author],
    min_count: int = 2,
) -> dict[str, Any]:
    users: dict[str, Any] = {}
    for user, count in counter.most_common():
        if count >= min_count:
            author = authors[user]
            users[user] = {
                "login": user,
                "count": count,
                "avatarUrl": author.avatarUrl,
                "url": author.url,
            }
    return users


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
    g = Github(settings.github_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)

    pr_nodes = get_pr_nodes(settings=settings)
    contributors_results = get_contributors(pr_nodes=pr_nodes)
    authors = contributors_results.authors

    top_contributors = get_users_to_write(
        counter=contributors_results.contributors,
        authors=authors,
    )

    top_translators = get_users_to_write(
        counter=contributors_results.translators,
        authors=authors,
    )
    top_translations_reviewers = get_users_to_write(
        counter=contributors_results.translation_reviewers,
        authors=authors,
    )

    # For local development
    # contributors_path = Path("../docs/en/data/contributors.yml")
    contributors_path = Path("./docs/en/data/contributors.yml")
    # translators_path = Path("../docs/en/data/translators.yml")
    translators_path = Path("./docs/en/data/translators.yml")
    # translation_reviewers_path = Path("../docs/en/data/translation_reviewers.yml")
    translation_reviewers_path = Path("./docs/en/data/translation_reviewers.yml")

    updated = [
        update_content(content_path=contributors_path, new_content=top_contributors),
        update_content(content_path=translators_path, new_content=top_translators),
        update_content(
            content_path=translation_reviewers_path,
            new_content=top_translations_reviewers,
        ),
    ]

    if not any(updated):
        logging.info("The data hasn't changed, finishing.")
        return

    logging.info("Setting up GitHub Actions git user")
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions@github.com"], check=True
    )
    branch_name = f"fastapi-people-contributors-{secrets.token_hex(4)}"
    logging.info(f"Creating a new branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    logging.info("Adding updated file")
    subprocess.run(
        [
            "git",
            "add",
            str(contributors_path),
            str(translators_path),
            str(translation_reviewers_path),
        ],
        check=True,
    )
    logging.info("Committing updated file")
    message = "👥 Update FastAPI People - Contributors and Translators"
    subprocess.run(["git", "commit", "-m", message], check=True)
    logging.info("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    logging.info("Creating PR")
    pr = repo.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")
    logging.info("Finished")


if __name__ == "__main__":
    main()
