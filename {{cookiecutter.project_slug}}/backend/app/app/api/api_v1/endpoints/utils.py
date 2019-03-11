from fastapi import APIRouter, Depends
from pydantic.types import EmailStr

from app.api.utils.security import get_current_active_superuser
from app.core.celery_app import celery_app
from app.models.msg import Msg
from app.models.user import UserInDB
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-celery/", tags=["utils"], response_model=Msg, status_code=201)
def test_celery(
    msg: Msg, current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test Celery worker
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", tags=["utils"], response_model=Msg, status_code=201)
def test_email(
    email_to: EmailStr, current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test emails
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
