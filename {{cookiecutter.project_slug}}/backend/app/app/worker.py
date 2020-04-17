from raven import Client

from app.core.config import settings
from app.core.celery_app import celery_app

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str):
    return f"test task return {word}"
