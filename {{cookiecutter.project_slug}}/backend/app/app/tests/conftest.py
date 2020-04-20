from typing import Dict, Iterator

import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_server_api, get_superuser_token_headers


@pytest.fixture(scope="session")
def db() -> Iterator[Session]:
    yield SessionLocal()


@pytest.fixture(scope="module")
def server_api() -> str:
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers() -> Dict[str, str]:
    return get_superuser_token_headers()


@pytest.fixture(scope="module")
def normal_user_token_headers(db: Session) -> Dict[str, str]:
    return authentication_token_from_email(email=settings.EMAIL_TEST_USER, db=db)
