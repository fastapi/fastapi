from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Form
from pydantic import BaseModel

app = FastAPI()
auth_router = APIRouter()


class AccountBase(BaseModel):
    username: str


class PasswordLogin(AccountBase):
    password: str


class TokenLogin(AccountBase):
    token: str


def register_form_post(
    router: APIRouter,
    path: str,
    schema: type[AccountBase],
):
    @router.post(path)
    def authenticate(
        data: Annotated[
            AccountBase,
            Form(),
            Depends(schema),
        ],
    ):
        return data

    return authenticate


register_form_post(
    auth_router,
    "/session/password/",
    PasswordLogin,
)
register_form_post(
    auth_router,
    "/session/token/",
    TokenLogin,
)
app.include_router(
    auth_router,
    prefix="/auth",
)
