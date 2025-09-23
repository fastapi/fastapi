"""
GitHub Documentation Deployment Status and Preview Links Bot.

This script handles documentation deployment status updates and preview link generation
for pull requests. It integrates with GitHub's API to:
- Set commit statuses for documentation deployment
- Generate preview links for modified documentation pages
- Post detailed comments in PRs with links to modified pages

The script is designed to work with GitHub Actions and expects specific environment
variables to be set for configuration.
"""

import logging
import re

from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the documentation deployment bot.

    Attributes:
        github_repository: The GitHub repository in format 'owner/repo'
        github_token: GitHub token with permissions to update statuses and comments
        deploy_url: The base URL where docs are deployed (optional until deployment completes)
        commit_sha: The SHA hash of the commit being processed
        run_id: The GitHub Actions run ID for linking back to the workflow
        is_done: Boolean indicating if the deployment process is complete
    """

    github_repository: str
    github_token: SecretStr
    deploy_url: str | None = None
    commit_sha: str
    run_id: int
    is_done: bool = False


class LinkData(BaseModel):
    """
    Represents link information for modified documentation pages.

    Attributes:
        previous_link: URL to the live/production version of the page
        preview_link: URL to the preview/deployed version of the page
        en_link: URL to the English version of the page (for non-English pages)
    """

    previous_link: str
    preview_link: str
    en_link: str | None = None


def main() -> None:
    """
    Main function that orchestrates the documentation deployment status workflow.

    The function:
    1. Sets up logging and configuration
    2. Finds the PR associated with the commit
    3. Updates commit status based on deployment state
    4. Generates preview links for modified documentation files
    5. Posts a comprehensive comment with all relevant links
    """
    logging.basicConfig(level=logging.INFO)
    settings = Settings()

    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(settings.github_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    use_pr = next(
        (pr for pr in repo.get_pulls() if pr.head.sha == settings.commit_sha), None
    )
    if not use_pr:
        logging.error(f"No PR found for hash: {settings.commit_sha}")
        return
    commits = list(use_pr.get_commits())
    current_commit = [c for c in commits if c.sha == settings.commit_sha][0]
    run_url = f"https://github.com/{settings.github_repository}/actions/runs/{settings.run_id}"
    if settings.is_done and not settings.deploy_url:
        current_commit.create_status(
            state="success",
            description="No Docs Changes",
            context="deploy-docs",
            target_url=run_url,
        )
        logging.info("No docs changes found")
        return
    if not settings.deploy_url:
        current_commit.create_status(
            state="pending",
            description="Deploying Docs",
            context="deploy-docs",
            target_url=run_url,
        )
        logging.info("No deploy URL available yet")
        return
    current_commit.create_status(
        state="success",
        description="Docs Deployed",
        context="deploy-docs",
        target_url=run_url,
    )

    files = list(use_pr.get_files())
    docs_files = [f for f in files if f.filename.startswith("docs/")]

    deploy_url = settings.deploy_url.rstrip("/")
    lang_links: dict[str, list[LinkData]] = {}
    for f in docs_files:
        match = re.match(r"docs/([^/]+)/docs/(.*)", f.filename)
        if not match:
            continue
        lang = match.group(1)
        path = match.group(2)
        if path.endswith("index.md"):
            path = path.replace("index.md", "")
        else:
            path = path.replace(".md", "/")
        en_path = path
        if lang == "en":
            use_path = en_path
        else:
            use_path = f"{lang}/{path}"
        link = LinkData(
            previous_link=f"https://fastapi.tiangolo.com/{use_path}",
            preview_link=f"{deploy_url}/{use_path}",
        )
        if lang != "en":
            link.en_link = f"https://fastapi.tiangolo.com/{en_path}"
        lang_links.setdefault(lang, []).append(link)

    links: list[LinkData] = []
    en_links = lang_links.get("en", [])
    en_links.sort(key=lambda x: x.preview_link)
    links.extend(en_links)

    langs = list(lang_links.keys())
    langs.sort()
    for lang in langs:
        if lang == "en":
            continue
        current_lang_links = lang_links[lang]
        current_lang_links.sort(key=lambda x: x.preview_link)
        links.extend(current_lang_links)

    message = f"📝 Docs preview for commit {settings.commit_sha} at: {deploy_url}"

    if links:
        message += "\n\n### Modified Pages\n\n"
        for link in links:
            message += f"* {link.preview_link}"
            message += f" - ([before]({link.previous_link}))"
            if link.en_link:
                message += f" - ([English]({link.en_link}))"
            message += "\n"

    print(message)
    use_pr.as_issue().create_comment(message)

    logging.info("Finished")


if __name__ == "__main__":
    main()
