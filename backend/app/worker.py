import sentry_sdk

from app.core.celery_app import celery_app
from app.core.config import settings

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN))


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"
