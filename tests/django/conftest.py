import django
import pytest
from django.conf import settings
from django.core.management.color import no_style
from django.core.management.sql import sql_flush
from django.db import connection

settings.configure(
    SECRET_KEY="not_very",
    ROOT_URLCONF="tests.django.proj.urls",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
    ],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)

django.setup()


@pytest.fixture(scope="session", autouse=True)
def django_db_setup():
    connection.creation.create_test_db(verbosity=0, autoclobber=True)

    yield

    connection.creation.destroy_test_db("default", verbosity=0)


@pytest.fixture(autouse=True)
def flush_db():
    sql_list = sql_flush(no_style(), connection, allow_cascade=False)

    connection.ops.execute_sql_flush(sql_list)


@pytest.fixture
def authenticated_session_id():
    from django.contrib.auth.models import User

    from tests.django.utils import create_authenticated_session

    user = User.objects.create_user(username="test", password="test")

    return create_authenticated_session(user)
