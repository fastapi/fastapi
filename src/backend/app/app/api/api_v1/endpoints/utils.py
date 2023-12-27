from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.core.celery_app import celery_app
from app.models import Message
from app.utils import send_test_email

router = APIRouter()


@router.post(
    "/test-celery/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_celery(body: Message) -> Message:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[body.message])
    return Message(message="Word received")


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return Message(message="Test email sent")
