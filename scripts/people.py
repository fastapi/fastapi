import logging
import secrets
import subprocess
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Container, Union

import httpx
import yaml
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

github_graphql_url = "https://api.github.com/graphql"
questions_category_id = "MDE4OkRpc2N1c3Npb25DYXRlZ29yeTMyMDAxNDM0"

discussions_query = """
query Q($after: String, $category_id: ID) {
  repository(name: "fastapi", owner: "fastapi") {
    discussions(first: 100, after: $after, categoryId: $category_id) {
      edges {
        cursor
        node {
          number
          author {
            login
            avatarUrl
            url
          }
          createdAt
          comments(first: 50) {
            totalCount
            nodes {
              createdAt
              author {
                login
                avatarUrl
                url
              }
              isAnswer
              replies(first: 10) {
                totalCount
                nodes {
                  createdAt
                  author {
                    login
                    avatarUrl
                    url
                  }
                }
              }
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
    avatarUrl: str | None = None
    url: str | None = None


class CommentsNode(BaseModel):
    createdAt: datetime
    author: Union[Author, None] = None


class Replies(BaseModel):
    totalCount: int
    nodes: list[CommentsNode]


class DiscussionsCommentsNode(CommentsNode):
    replies: Replies


class DiscussionsComments(BaseModel):
    totalCount: int
    nodes: list[DiscussionsCommentsNode]


class DiscussionsNode(BaseModel):
    number: int
    author: Union[Author, None] = None
    title: str | None = None
    createdAt: datetime
    comments: DiscussionsComments


class DiscussionsEdge(BaseModel):
    cursor: str
    node: DiscussionsNode


class Discussions(BaseModel):
    edges: list[DiscussionsEdge]


class DiscussionsRepository(BaseModel):
    discussions: Discussions


class DiscussionsResponseData(BaseModel):
    repository: DiscussionsRepository


class DiscussionsResponse(BaseModel):
    data: DiscussionsResponseData


class Settings(BaseSettings):
    github_token: SecretStr
    github_repository: str
    httpx_timeout: int = 30
    sleep_interval: int = 5


def get_graphql_response(
    *,
    settings: Settings,
    query: str,
    after: Union[str, None] = None,
    category_id: Union[str, None] = None,
) -> dict[str, Any]:
    headers = {"Authorization": f"token {settings.github_token.get_secret_value()}"}
    variables = {"after": after, "category_id": category_id}
    response = httpx.post(
        github_graphql_url,
        headers=headers,
        timeout=settings.httpx_timeout,
        json={"query": query, "variables": variables, "operationName": "Q"},
    )
    if response.status_code != 200:
        logging.error(
            f"Response was not 200, after: {after}, category_id: {category_id}"
        )
        logging.error(response.text)
        raise RuntimeError(response.text)
    data = response.json()
    if "errors" in data:
        logging.error(f"Errors in response, after: {after}, category_id: {category_id}")
        logging.error(data["errors"])
        logging.error(response.text)
        raise RuntimeError(response.text)
    return data


def get_graphql_question_discussion_edges(
    *,
    settings: Settings,
    after: Union[str, None] = None,
) -> list[DiscussionsEdge]:
    data = get_graphql_response(
        settings=settings,
        query=discussions_query,
        after=after,
        category_id=questions_category_id,
    )
    graphql_response = DiscussionsResponse.model_validate(data)
    return graphql_response.data.repository.discussions.edges


class DiscussionExpertsResults(BaseModel):
    commenters: Counter[str]
    last_month_commenters: Counter[str]
    three_months_commenters: Counter[str]
    six_months_commenters: Counter[str]
    one_year_commenters: Counter[str]
    authors: dict[str, Author]


def get_discussion_nodes(settings: Settings) -> list[DiscussionsNode]:
    discussion_nodes: list[DiscussionsNode] = []
    discussion_edges = get_graphql_question_discussion_edges(settings=settings)

    while discussion_edges:
        for discussion_edge in discussion_edges:
            discussion_nodes.append(discussion_edge.node)
        last_edge = discussion_edges[-1]
        # Handle GitHub secondary rate limits, requests per minute
        time.sleep(settings.sleep_interval)
        discussion_edges = get_graphql_question_discussion_edges(
            settings=settings, after=last_edge.cursor
        )
    return discussion_nodes


def get_discussions_experts(
    discussion_nodes: list[DiscussionsNode],
) -> DiscussionExpertsResults:
    commenters = Counter[str]()
    last_month_commenters = Counter[str]()
    three_months_commenters = Counter[str]()
    six_months_commenters = Counter[str]()
    one_year_commenters = Counter[str]()
    authors: dict[str, Author] = {}

    now = datetime.now(tz=timezone.utc)
    one_month_ago = now - timedelta(days=30)
    three_months_ago = now - timedelta(days=90)
    six_months_ago = now - timedelta(days=180)
    one_year_ago = now - timedelta(days=365)

    for discussion in discussion_nodes:
        discussion_author_name = None
        if discussion.author:
            authors[discussion.author.login] = discussion.author
            discussion_author_name = discussion.author.login
        discussion_commentors: dict[str, datetime] = {}
        for comment in discussion.comments.nodes:
            if comment.author:
                authors[comment.author.login] = comment.author
                if comment.author.login != discussion_author_name:
                    author_time = discussion_commentors.get(
                        comment.author.login, comment.createdAt
                    )
                    discussion_commentors[comment.author.login] = max(
                        author_time, comment.createdAt
                    )
            for reply in comment.replies.nodes:
                if reply.author:
                    authors[reply.author.login] = reply.author
                    if reply.author.login != discussion_author_name:
                        author_time = discussion_commentors.get(
                            reply.author.login, reply.createdAt
                        )
                        discussion_commentors[reply.author.login] = max(
                            author_time, reply.createdAt
                        )
        for author_name, author_time in discussion_commentors.items():
            commenters[author_name] += 1
            if author_time > one_month_ago:
                last_month_commenters[author_name] += 1
            if author_time > three_months_ago:
                three_months_commenters[author_name] += 1
            if author_time > six_months_ago:
                six_months_commenters[author_name] += 1
            if author_time > one_year_ago:
                one_year_commenters[author_name] += 1
    discussion_experts_results = DiscussionExpertsResults(
        authors=authors,
        commenters=commenters,
        last_month_commenters=last_month_commenters,
        three_months_commenters=three_months_commenters,
        six_months_commenters=six_months_commenters,
        one_year_commenters=one_year_commenters,
    )
    return discussion_experts_results


def get_top_users(
    *,
    counter: Counter[str],
    authors: dict[str, Author],
    skip_users: Container[str],
    min_count: int = 2,
) -> list[dict[str, Any]]:
    users: list[dict[str, Any]] = []
    for commenter, count in counter.most_common(50):
        if commenter in skip_users:
            continue
        if count >= min_count:
            author = authors[commenter]
            users.append(
                {
                    "login": commenter,
                    "count": count,
                    "avatarUrl": author.avatarUrl,
                    "url": author.url,
                }
            )
    return users


def get_users_to_write(
    *,
    counter: Counter[str],
    authors: dict[str, Author],
    min_count: int = 2,
) -> list[dict[str, Any]]:
    users: dict[str, Any] = {}
    users_list: list[dict[str, Any]] = []
    for user, count in counter.most_common(60):
        if count >= min_count:
            author = authors[user]
            user_data = {
                "login": user,
                "count": count,
                "avatarUrl": author.avatarUrl,
                "url": author.url,
            }
            users[user] = user_data
            users_list.append(user_data)
    return users_list


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

    discussion_nodes = get_discussion_nodes(settings=settings)
    experts_results = get_discussions_experts(discussion_nodes=discussion_nodes)

    authors = experts_results.authors
    maintainers_logins = {"tiangolo"}
    maintainers = []
    for login in maintainers_logins:
        user = authors[login]
        maintainers.append(
            {
                "login": login,
                "answers": experts_results.commenters[login],
                "avatarUrl": user.avatarUrl,
                "url": user.url,
            }
        )

    experts = get_users_to_write(
        counter=experts_results.commenters,
        authors=authors,
    )
    last_month_experts = get_users_to_write(
        counter=experts_results.last_month_commenters,
        authors=authors,
    )
    three_months_experts = get_users_to_write(
        counter=experts_results.three_months_commenters,
        authors=authors,
    )
    six_months_experts = get_users_to_write(
        counter=experts_results.six_months_commenters,
        authors=authors,
    )
    one_year_experts = get_users_to_write(
        counter=experts_results.one_year_commenters,
        authors=authors,
    )

    people = {
        "maintainers": maintainers,
        "experts": experts,
        "last_month_experts": last_month_experts,
        "three_months_experts": three_months_experts,
        "six_months_experts": six_months_experts,
        "one_year_experts": one_year_experts,
    }

    # For local development
    # people_path = Path("../docs/en/data/people.yml")
    people_path = Path("./docs/en/data/people.yml")

    updated = update_content(content_path=people_path, new_content=people)

    if not updated:
        logging.info("The data hasn't changed, finishing.")
        return

    logging.info("Setting up GitHub Actions git user")
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions@github.com"], check=True
    )
    branch_name = f"fastapi-people-experts-{secrets.token_hex(4)}"
    logging.info(f"Creating a new branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    logging.info("Adding updated file")
    subprocess.run(["git", "add", str(people_path)], check=True)
    logging.info("Committing updated file")
    message = "👥 Update FastAPI People - Experts"
    subprocess.run(["git", "commit", "-m", message], check=True)
    logging.info("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    logging.info("Creating PR")
    pr = repo.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")
    logging.info("Finished")


if __name__ == "__main__":
    main()
