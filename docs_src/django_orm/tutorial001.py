import os

import django
from asgiref.sync import sync_to_async
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from polls.models import Question  # noqa: I001 E402


app = FastAPI()


@app.get("/questions")
def get_questions():
    questions = Question.objects.all()

    return [{"question": question.question_text} for question in questions]


@app.get("/questions-async")
async def get_questions_async():
    def _fetch_questions():
        return list(Question.objects.all())

    questions = await sync_to_async(_fetch_questions)()

    return [{"question": question.question_text} for question in questions]


@app.get("/questions/{question_id}")
async def get_question(question_id: int):
    question = await Question.objects.filter(id=question_id).afirst()

    return {"question": question.question_text}
