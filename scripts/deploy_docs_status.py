import logging
import re
from typing import Literal

from github import Auth, Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_repository: str
    github_token: SecretStr
    deploy_url: str | None = None
    commit_sha: str
    run_id: int
    state: Literal["pending", "success", "error"] = "pending"


class LinkData(BaseModel):
    previous_link: str
    preview_link: str
    en_link: str | None = None


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()

    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(auth=Auth.Token(settings.github_token.get_secret_value()))
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
    if settings.state == "pending":
        current_commit.create_status(
            state="pending",
            description="Deploying Docs",
            context="deploy-docs",
            target_url=run_url,
        )
        logging.info("No deploy URL available yet")
        return
    if settings.state == "error":
        current_commit.create_status(
            state="error",
            description="Error Deploying Docs",
            context="deploy-docs",
            target_url=run_url,
        )
        logging.info("Error deploying docs")
        return
    assert settings.state == "success"
    if not settings.deploy_url:
        current_commit.create_status(
            state="success",
            description="No Docs Changes",
            context="deploy-docs",
            target_url=run_url,
        )
        logging.info("No docs changes found")
        return
    assert settings.deploy_url
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

    header = "## 📝 Docs preview"
    message = header
    message += f"\n\nLast commit {settings.commit_sha} at: {deploy_url}"

    if links:
        message += "\n\n### Modified Pages\n\n"
        for link in links:
            message += f"* {link.preview_link}"
            message += f" - ([before]({link.previous_link}))"
            if link.en_link:
                message += f" - ([English]({link.en_link}))"
            message += "\n"

    print(message)
    issue = use_pr.as_issue()
    comments = list(issue.get_comments())
    for comment in comments:
        if (
            comment.body.startswith(header)
            and comment.user.login == "github-actions[bot]"
        ):
            comment.edit(message)
            break
    else:
        issue.create_comment(message)

    logging.info("Finished")


if __name__ == "__main__":
    main()
