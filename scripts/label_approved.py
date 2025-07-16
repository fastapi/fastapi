import logging
from typing import Literal

from github import Github
from github.PullRequestReview import PullRequestReview
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class LabelSettings(BaseModel):
    await_label: str | None = None
    number: int


default_config = {"approved-2": LabelSettings(await_label="awaiting-review", number=2)}


class Settings(BaseSettings):
    github_repository: str
    token: SecretStr
    debug: bool | None = False
    config: dict[str, LabelSettings] | Literal[""] = default_config


settings = Settings()
if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logging.debug(f"Using config: {settings.model_dump_json()}")
g = Github(settings.token.get_secret_value())
repo = g.get_repo(settings.github_repository)
for pr in repo.get_pulls(state="open"):
    logging.info(f"Checking PR: #{pr.number}")
    pr_labels = list(pr.get_labels())
    pr_label_by_name = {label.name: label for label in pr_labels}
    reviews = list(pr.get_reviews())
    review_by_user: dict[str, PullRequestReview] = {}
    for review in reviews:
        if review.user.login in review_by_user:
            stored_review = review_by_user[review.user.login]
            if review.submitted_at >= stored_review.submitted_at:
                review_by_user[review.user.login] = review
        else:
            review_by_user[review.user.login] = review
    approved_reviews = [
        review for review in review_by_user.values() if review.state == "APPROVED"
    ]
    config = settings.config or default_config
    for approved_label, conf in config.items():
        logging.debug(f"Processing config: {conf.model_dump_json()}")
        if conf.await_label is None or (conf.await_label in pr_label_by_name):
            logging.debug(f"Processable PR: {pr.number}")
            if len(approved_reviews) >= conf.number:
                logging.info(f"Adding label to PR: {pr.number}")
                pr.add_to_labels(approved_label)
                if conf.await_label:
                    logging.info(f"Removing label from PR: {pr.number}")
                    pr.remove_from_labels(conf.await_label)
logging.info("Finished")
