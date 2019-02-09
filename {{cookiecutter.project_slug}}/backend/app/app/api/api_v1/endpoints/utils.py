from fastapi import APIRouter, Depends
from pydantic.types import EmailStr
from starlette.exceptions import HTTPException

from app.core.celery_app import celery_app
from app.core.jwt import get_current_user
from app.crud.user import check_if_user_is_superuser
from app.models.msg import Msg
from app.models.user import UserInDB
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-celery/", tags=["utils"], response_model=Msg, status_code=201)
def route_test_celery(msg: Msg, current_user: UserInDB = Depends(get_current_user)):
    """
    Test Celery worker
    """
    if not check_if_user_is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not a superuser")
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", tags=["utils"], response_model=Msg, status_code=201)
def route_test_email(
    email_to: EmailStr, current_user: UserInDB = Depends(get_current_user)
):
    """
    Test emails
    """
    if not check_if_user_is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not a superuser")
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
