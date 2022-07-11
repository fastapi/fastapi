import logging
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Container, DefaultDict, Dict, List, Set, Union

import httpx
import yaml
from github import Github
from pydantic import BaseModel, BaseSettings, SecretStr

github_graphql_url = "https://api.github.com/graphql"

issues_query = """
query Q($after: String) {
  repository(name: "fastapi", owner: "tiangolo") {
    issues(first: 100, after: $after) {
      edges {
        cursor
        node {
          number
          author {
            login
            avatarUrl
            url
          }
          title
          createdAt
          state
          comments(first: 100) {
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
"""

prs_query = """
query Q($after: String) {
  repository(name: "fastapi", owner: "tiangolo") {
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
          state
          comments(first: 100) {
            nodes {
              createdAt
              author {
                login
                avatarUrl
                url
              }
            }
          }
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


class Author(BaseModel):
    login: str
    avatarUrl: str
    url: str


class CommentsNode(BaseModel):
    createdAt: datetime
    author: Union[Author, None] = None


class Comments(BaseModel):
    nodes: List[CommentsNode]


class IssuesNode(BaseModel):
    number: int
    author: Union[Author, None] = None
    title: str
    createdAt: datetime
    state: str
    comments: Comments


class IssuesEdge(BaseModel):
    cursor: str
    node: IssuesNode


class Issues(BaseModel):
    edges: List[IssuesEdge]


class IssuesRepository(BaseModel):
    issues: Issues


class IssuesResponseData(BaseModel):
    repository: IssuesRepository


class IssuesResponse(BaseModel):
    data: IssuesResponseData


class LabelNode(BaseModel):
    name: str


class Labels(BaseModel):
    nodes: List[LabelNode]


class ReviewNode(BaseModel):
    author: Union[Author, None] = None
    state: str


class Reviews(BaseModel):
    nodes: List[ReviewNode]


class PullRequestNode(BaseModel):
    number: int
    labels: Labels
    author: Union[Author, None] = None
    title: str
    createdAt: datetime
    state: str
    comments: Comments
    reviews: Reviews


class PullRequestEdge(BaseModel):
    cursor: str
    node: PullRequestNode


class PullRequests(BaseModel):
    edges: List[PullRequestEdge]


class PRsRepository(BaseModel):
    pullRequests: PullRequests


class PRsResponseData(BaseModel):
    repository: PRsRepository


class PRsResponse(BaseModel):
    data: PRsResponseData


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
    edges: List[SponsorshipAsMaintainerEdge]


class SponsorsUser(BaseModel):
    sponsorshipsAsMaintainer: SponsorshipAsMaintainer


class SponsorsResponseData(BaseModel):
    user: SponsorsUser


class SponsorsResponse(BaseModel):
    data: SponsorsResponseData


class Settings(BaseSettings):
    input_token: SecretStr
    input_standard_token: SecretStr
    github_repository: str


def get_graphql_response(
    *, settings: Settings, query: str, after: Union[str, None] = None
):
    headers = {"Authorization": f"token {settings.input_token.get_secret_value()}"}
    variables = {"after": after}
    response = httpx.post(
        github_graphql_url,
        headers=headers,
        json={"query": query, "variables": variables, "operationName": "Q"},
    )
    if not response.status_code == 200:
        logging.error(f"Response was not 200, after: {after}")
        logging.error(response.text)
        raise RuntimeError(response.text)
    data = response.json()
    return data


def get_graphql_issue_edges(*, settings: Settings, after: Union[str, None] = None):
    data = get_graphql_response(settings=settings, query=issues_query, after=after)
    graphql_response = IssuesResponse.parse_obj(data)
    return graphql_response.data.repository.issues.edges


def get_graphql_pr_edges(*, settings: Settings, after: Union[str, None] = None):
    data = get_graphql_response(settings=settings, query=prs_query, after=after)
    graphql_response = PRsResponse.parse_obj(data)
    return graphql_response.data.repository.pullRequests.edges


def get_graphql_sponsor_edges(*, settings: Settings, after: Union[str, None] = None):
    data = get_graphql_response(settings=settings, query=sponsors_query, after=after)
    graphql_response = SponsorsResponse.parse_obj(data)
    return graphql_response.data.user.sponsorshipsAsMaintainer.edges


def get_experts(settings: Settings):
    issue_nodes: List[IssuesNode] = []
    issue_edges = get_graphql_issue_edges(settings=settings)

    while issue_edges:
        for edge in issue_edges:
            issue_nodes.append(edge.node)
        last_edge = issue_edges[-1]
        issue_edges = get_graphql_issue_edges(settings=settings, after=last_edge.cursor)

    commentors = Counter()
    last_month_commentors = Counter()
    authors: Dict[str, Author] = {}

    now = datetime.now(tz=timezone.utc)
    one_month_ago = now - timedelta(days=30)

    for issue in issue_nodes:
        issue_author_name = None
        if issue.author:
            authors[issue.author.login] = issue.author
            issue_author_name = issue.author.login
        issue_commentors = set()
        for comment in issue.comments.nodes:
            if comment.author:
                authors[comment.author.login] = comment.author
                if comment.author.login == issue_author_name:
                    continue
                issue_commentors.add(comment.author.login)
        for author_name in issue_commentors:
            commentors[author_name] += 1
            if issue.createdAt > one_month_ago:
                last_month_commentors[author_name] += 1
    return commentors, last_month_commentors, authors


def get_contributors(settings: Settings):
    pr_nodes: List[PullRequestNode] = []
    pr_edges = get_graphql_pr_edges(settings=settings)

    while pr_edges:
        for edge in pr_edges:
            pr_nodes.append(edge.node)
        last_edge = pr_edges[-1]
        pr_edges = get_graphql_pr_edges(settings=settings, after=last_edge.cursor)

    contributors = Counter()
    commentors = Counter()
    reviewers = Counter()
    authors: Dict[str, Author] = {}

    for pr in pr_nodes:
        author_name = None
        if pr.author:
            authors[pr.author.login] = pr.author
            author_name = pr.author.login
        pr_commentors: Set[str] = set()
        pr_reviewers: Set[str] = set()
        for comment in pr.comments.nodes:
            if comment.author:
                authors[comment.author.login] = comment.author
                if comment.author.login == author_name:
                    continue
                pr_commentors.add(comment.author.login)
        for author_name in pr_commentors:
            commentors[author_name] += 1
        for review in pr.reviews.nodes:
            if review.author:
                authors[review.author.login] = review.author
                pr_reviewers.add(review.author.login)
        for reviewer in pr_reviewers:
            reviewers[reviewer] += 1
        if pr.state == "MERGED" and pr.author:
            contributors[pr.author.login] += 1
    return contributors, commentors, reviewers, authors


def get_individual_sponsors(settings: Settings):
    nodes: List[SponsorshipAsMaintainerNode] = []
    edges = get_graphql_sponsor_edges(settings=settings)

    while edges:
        for edge in edges:
            nodes.append(edge.node)
        last_edge = edges[-1]
        edges = get_graphql_sponsor_edges(settings=settings, after=last_edge.cursor)

    tiers: DefaultDict[float, Dict[str, SponsorEntity]] = defaultdict(dict)
    for node in nodes:
        tiers[node.tier.monthlyPriceInDollars][
            node.sponsorEntity.login
        ] = node.sponsorEntity
    return tiers


def get_top_users(
    *,
    counter: Counter,
    min_count: int,
    authors: Dict[str, Author],
    skip_users: Container[str],
):
    users = []
    for commentor, count in counter.most_common(50):
        if commentor in skip_users:
            continue
        if count >= min_count:
            author = authors[commentor]
            users.append(
                {
                    "login": commentor,
                    "count": count,
                    "avatarUrl": author.avatarUrl,
                    "url": author.url,
                }
            )
    return users


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    g = Github(settings.input_standard_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    issue_commentors, issue_last_month_commentors, issue_authors = get_experts(
        settings=settings
    )
    contributors, pr_commentors, reviewers, pr_authors = get_contributors(
        settings=settings
    )
    authors = {**issue_authors, **pr_authors}
    maintainers_logins = {"tiangolo"}
    bot_names = {"codecov", "github-actions"}
    maintainers = []
    for login in maintainers_logins:
        user = authors[login]
        maintainers.append(
            {
                "login": login,
                "answers": issue_commentors[login],
                "prs": contributors[login],
                "avatarUrl": user.avatarUrl,
                "url": user.url,
            }
        )

    min_count_expert = 10
    min_count_last_month = 3
    min_count_contributor = 4
    min_count_reviewer = 4
    skip_users = maintainers_logins | bot_names
    experts = get_top_users(
        counter=issue_commentors,
        min_count=min_count_expert,
        authors=authors,
        skip_users=skip_users,
    )
    last_month_active = get_top_users(
        counter=issue_last_month_commentors,
        min_count=min_count_last_month,
        authors=authors,
        skip_users=skip_users,
    )
    top_contributors = get_top_users(
        counter=contributors,
        min_count=min_count_contributor,
        authors=authors,
        skip_users=skip_users,
    )
    top_reviewers = get_top_users(
        counter=reviewers,
        min_count=min_count_reviewer,
        authors=authors,
        skip_users=skip_users,
    )

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

    people = {
        "maintainers": maintainers,
        "experts": experts,
        "last_month_active": last_month_active,
        "top_contributors": top_contributors,
        "top_reviewers": top_reviewers,
    }
    github_sponsors = {
        "sponsors": sponsors,
    }
    people_path = Path("./docs/en/data/people.yml")
    github_sponsors_path = Path("./docs/en/data/github_sponsors.yml")
    people_old_content = people_path.read_text(encoding="utf-8")
    github_sponsors_old_content = github_sponsors_path.read_text(encoding="utf-8")
    new_people_content = yaml.dump(
        people, sort_keys=False, width=200, allow_unicode=True
    )
    new_github_sponsors_content = yaml.dump(
        github_sponsors, sort_keys=False, width=200, allow_unicode=True
    )
    if (
        people_old_content == new_people_content
        and github_sponsors_old_content == new_github_sponsors_content
    ):
        logging.info("The FastAPI People data hasn't changed, finishing.")
        sys.exit(0)
    people_path.write_text(new_people_content, encoding="utf-8")
    github_sponsors_path.write_text(new_github_sponsors_content, encoding="utf-8")
    logging.info("Setting up GitHub Actions git user")
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions@github.com"], check=True
    )
    branch_name = "fastapi-people"
    logging.info(f"Creating a new branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    logging.info("Adding updated file")
    subprocess.run(
        ["git", "add", str(people_path), str(github_sponsors_path)], check=True
    )
    logging.info("Committing updated file")
    message = "👥 Update FastAPI People"
    result = subprocess.run(["git", "commit", "-m", message], check=True)
    logging.info("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    logging.info("Creating PR")
    pr = repo.create_pull(title=message, body=message, base="master", head=branch_name)
    logging.info(f"Created PR: {pr.number}")
    logging.info("Finished")
