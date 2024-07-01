# Using the Django ORM with FastAPI

In this guide we'll show you how to use Django's ORM with FastAPI.

This can be extremely useful when migrating from Django to FastAPI, as you can reuse your existing Django models and queries. It's also a great way to take advantage of Django's powerful ORM while using FastAPI's modern features.

This tutorial is based on the Django polls tutorial, but you can apply the same concepts to any Django project.

## Prerequisites

- A Django project like the one created from the [Django polls tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- Basic knowledge of FastAPI

## Step 1: Install FastAPI

First, let's install FastAPI in our Django project:

```bash
# make sure to run this in your Django virtual environment
pip install fastapi
```

## Step 2: Set up a basic FastAPI application

Create a `main.py` file:

```python
from fastapi import FastAPI

app = FastAPI()
```

In the next steps we'll import the `Question` model from Django, and create a FastAPI endpoint to list all questions.

## Step 3: Import Django models

In your `main.py` file, let's import the `Question` model:

```python
from polls.models import Question
```

Make sure to replace `polls` with the name of your Django app.

## Step 4: Create a FastAPI endpoint

Now let's create a FastAPI endpoint to list all questions:

```python
@app.get("/questions")
def get_questions():
    questions = Question.objects.all()

    return [{"question": question.question_text} for question in questions]
```

## Step 5: Run the FastAPI application

No we can run the FastAPI application:

```bash
fastapi dev main.py
```

If you go to `http://localhost:8000/questions` we should see the list of questions, right? 🤔

Unfortunately, we'll get an error:

```text
django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
```

This error happens because Django settings are not configured before importing the Django models.

## Step 6: Configure Django settings

To fix this error, we need to configure Django settings before importing the Django models.

In the `main.py` add the following code **before** importing the Django models:

```python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
```

This will configure Django settings before importing the Django models.

## Step 7: Run the FastAPI application

Now you can run the FastAPI application:

```bash
fastapi dev main.py
```

And now if we go to `http://localhost:8000/questions` we should see a list of questions! 🎉
