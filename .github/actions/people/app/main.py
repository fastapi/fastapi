import logging
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Container, DefaultDict, Dict, List, Set, Union

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
          title
          createdAt
          comments(first: 100) {
            nodes {
              createdAt
              author {
                login
                avatarUrl
                url
              }
              isAnswer
              replies(first: 10) {
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
  user(login: "fastapi") {
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


# Discussions


class CommentsNode(BaseModel):
    createdAt: datetime
    author: Union[Author, None] = None


class Replies(BaseModel):
    nodes: List[CommentsNode]


class DiscussionsCommentsNode(CommentsNode):
    replies: Replies


class Comments(BaseModel):
    nodes: List[CommentsNode]


class DiscussionsComments(BaseModel):
    nodes: List[DiscussionsCommentsNode]


class DiscussionsNode(BaseModel):
    number: int
    author: Union[Author, None] = None
    title: str
    createdAt: datetime
    comments: DiscussionsComments


class DiscussionsEdge(BaseModel):
    cursor: str
    node: DiscussionsNode


class Discussions(BaseModel):
    edges: List[DiscussionsEdge]


class DiscussionsRepository(BaseModel):
    discussions: Discussions


class DiscussionsResponseData(BaseModel):
    repository: DiscussionsRepository


class DiscussionsResponse(BaseModel):
    data: DiscussionsResponseData


# PRs


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


# Sponsors


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
    github_repository: str
    httpx_timeout: int = 30


def get_graphql_response(
    *,
    settings: Settings,
    query: str,
    after: Union[str, None] = None,
    category_id: Union[str, None] = None,
) -> Dict[str, Any]:
    headers = {"Authorization": f"token {settings.input_token.get_secret_value()}"}
    # category_id is only used by one query, but GraphQL allows unused variables, so
    # keep it here for simplicity
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
):
    data = get_graphql_response(
        settings=settings,
        query=discussions_query,
        after=after,
        category_id=questions_category_id,
    )
    graphql_response = DiscussionsResponse.model_validate(data)
    return graphql_response.data.repository.discussions.edges


def get_graphql_pr_edges(*, settings: Settings, after: Union[str, None] = None):
    data = get_graphql_response(settings=settings, query=prs_query, after=after)
    graphql_response = PRsResponse.model_validate(data)
    return graphql_response.data.repository.pullRequests.edges


def get_graphql_sponsor_edges(*, settings: Settings, after: Union[str, None] = None):
    data = get_graphql_response(settings=settings, query=sponsors_query, after=after)
    graphql_response = SponsorsResponse.model_validate(data)
    return graphql_response.data.user.sponsorshipsAsMaintainer.edges


class DiscussionExpertsResults(BaseModel):
    commenters: Counter
    last_month_commenters: Counter
    three_months_commenters: Counter
    six_months_commenters: Counter
    one_year_commenters: Counter
    authors: Dict[str, Author]


def get_discussion_nodes(settings: Settings) -> List[DiscussionsNode]:
    discussion_nodes: List[DiscussionsNode] = []
    discussion_edges = get_graphql_question_discussion_edges(settings=settings)

    while discussion_edges:
        for discussion_edge in discussion_edges:
            discussion_nodes.append(discussion_edge.node)
        last_edge = discussion_edges[-1]
        discussion_edges = get_graphql_question_discussion_edges(
            settings=settings, after=last_edge.cursor
        )
    return discussion_nodes


def get_discussions_experts(
    discussion_nodes: List[DiscussionsNode],
) -> DiscussionExpertsResults:
    commenters = Counter()
    last_month_commenters = Counter()
    three_months_commenters = Counter()
    six_months_commenters = Counter()
    one_year_commenters = Counter()
    authors: Dict[str, Author] = {}

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


def get_pr_nodes(settings: Settings) -> List[PullRequestNode]:
    pr_nodes: List[PullRequestNode] = []
    pr_edges = get_graphql_pr_edges(settings=settings)

    while pr_edges:
        for edge in pr_edges:
            pr_nodes.append(edge.node)
        last_edge = pr_edges[-1]
        pr_edges = get_graphql_pr_edges(settings=settings, after=last_edge.cursor)
    return pr_nodes


class ContributorsResults(BaseModel):
    contributors: Counter
    commenters: Counter
    reviewers: Counter
    translation_reviewers: Counter
    authors: Dict[str, Author]


def get_contributors(pr_nodes: List[PullRequestNode]) -> ContributorsResults:
    contributors = Counter()
    commenters = Counter()
    reviewers = Counter()
    translation_reviewers = Counter()
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
            commenters[author_name] += 1
        for review in pr.reviews.nodes:
            if review.author:
                authors[review.author.login] = review.author
                pr_reviewers.add(review.author.login)
                for label in pr.labels.nodes:
                    if label.name == "lang-all":
                        translation_reviewers[review.author.login] += 1
                        break
        for reviewer in pr_reviewers:
            reviewers[reviewer] += 1
        if pr.state == "MERGED" and pr.author:
            contributors[pr.author.login] += 1
    return ContributorsResults(
        contributors=contributors,
        commenters=commenters,
        reviewers=reviewers,
        translation_reviewers=translation_reviewers,
        authors=authors,
    )


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
        tiers[node.tier.monthlyPriceInDollars][node.sponsorEntity.login] = (
            node.sponsorEntity
        )
    return tiers


def get_top_users(
    *,
    counter: Counter,
    authors: Dict[str, Author],
    skip_users: Container[str],
    min_count: int = 2,
):
    users = []
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(settings.input_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    discussion_nodes = get_discussion_nodes(settings=settings)
    experts_results = get_discussions_experts(discussion_nodes=discussion_nodes)
    pr_nodes = get_pr_nodes(settings=settings)
    contributors_results = get_contributors(pr_nodes=pr_nodes)
    authors = {**experts_results.authors, **contributors_results.authors}
    maintainers_logins = {"tiangolo"}
    bot_names = {"codecov", "github-actions", "pre-commit-ci", "dependabot"}
    maintainers = []
    for login in maintainers_logins:
        user = authors[login]
        maintainers.append(
            {
                "login": login,
                "answers": experts_results.commenters[login],
                "prs": contributors_results.contributors[login],
                "avatarUrl": user.avatarUrl,
                "url": user.url,
            }
        )

    skip_users = maintainers_logins | bot_names
    experts = get_top_users(
        counter=experts_results.commenters,
        authors=authors,
        skip_users=skip_users,
    )
    last_month_experts = get_top_users(
        counter=experts_results.last_month_commenters,
        authors=authors,
        skip_users=skip_users,
    )
    three_months_experts = get_top_users(
        counter=experts_results.three_months_commenters,
        authors=authors,
        skip_users=skip_users,
    )
    six_months_experts = get_top_users(
        counter=experts_results.six_months_commenters,
        authors=authors,
        skip_users=skip_users,
    )
    one_year_experts = get_top_users(
        counter=experts_results.one_year_commenters,
        authors=authors,
        skip_users=skip_users,
    )
    top_contributors = get_top_users(
        counter=contributors_results.contributors,
        authors=authors,
        skip_users=skip_users,
    )
    top_reviewers = get_top_users(
        counter=contributors_results.reviewers,
        authors=authors,
        skip_users=skip_users,
    )
    top_translations_reviewers = get_top_users(
        counter=contributors_results.translation_reviewers,
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
        "last_month_experts": last_month_experts,
        "three_months_experts": three_months_experts,
        "six_months_experts": six_months_experts,
        "one_year_experts": one_year_experts,
        "top_contributors": top_contributors,
        "top_reviewers": top_reviewers,
        "top_translations_reviewers": top_translations_reviewers,
    }
    github_sponsors = {
        "sponsors": sponsors,
    }
    # For local development
    # people_path = Path("../../../../docs/en/data/people.yml")
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
