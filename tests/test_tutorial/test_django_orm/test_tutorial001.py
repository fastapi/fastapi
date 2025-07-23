import pathlib
import sys

import pytest
from django.core.management.color import no_style
from django.core.management.sql import sql_flush
from django.db import connection
from django.utils import timezone
from fastapi.testclient import TestClient

HERE = pathlib.Path(__file__).parent

sys.path.append(str(HERE.parents[2] / "docs_src" / "django_orm"))

from docs_src.django_orm.tutorial001 import Question, app  # noqa: I001 E402


client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def django_db_setup():
    connection.creation.create_test_db(verbosity=0, autoclobber=True)

    yield

    connection.creation.destroy_test_db("default", verbosity=0)


@pytest.fixture(autouse=True)
def flush_db():
    sql_list = sql_flush(no_style(), connection, allow_cascade=False)

    connection.ops.execute_sql_flush(sql_list)


def test_get_questions():
    Question.objects.create(question_text="there goes my hero", pub_date=timezone.now())

    response = client.get("/questions")

    assert response.status_code == 200, response.text
    assert response.json() == [{"question": "there goes my hero"}]


def test_question_empty():
    response = client.get("/questions")

    assert response.status_code == 200, response.text
    assert response.json() == []


def test_get_questions_async():
    Question.objects.create(question_text="everlong", pub_date=timezone.now())

    response = client.get("/questions-async")

    assert response.status_code == 200, response.text
    assert response.json() == [{"question": "everlong"}]


def test_get_single_question():
    question = Question.objects.create(question_text="my hero", pub_date=timezone.now())

    response = client.get(f"/questions/{question.id}")

    assert response.status_code == 200, response.text
    assert response.json() == {"question": "my hero"}
