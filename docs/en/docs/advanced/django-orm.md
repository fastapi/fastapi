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

Let's create a basic FastAPI application in a new file called `main.py`:

//// tab | Python 3.8+

```Python
{!> ../../../docs_src/django_orm/tutorial001.py[ln:5,13]!}
```

In the next steps we'll import the `Question` model from Django, and create a FastAPI endpoint to list all questions.

## Step 3: Import and use Django models

In your `main.py` file, let's import the `Question` model and create a FastAPI endpoint to list all questions:

//// tab | Python 3.8+

```Python
{!> ../../../docs_src/django_orm/tutorial001.py[ln:10,16-20]!}
```

## Step 4: Run the FastAPI application

Now, let's run the FastAPI application:

```bash
fastapi dev main.py
```

If you go to `http://localhost:8000/questions` we should see the list of questions, right? 🤔

Unfortunately, we'll get this error:

```text
django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured.
You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
```

This error happens because Django needs to be configured before importing the models.

## Step 5: Configure Django settings

To fix this error, we need to configure Django settings before importing the Django models.

In the `main.py` add the following code **before** importing the Django models:

//// tab | Python 3.8+

```Python
{!> ../../../docs_src/django_orm/tutorial001.py[ln:1,7-10]!}
```

Now, if you run the FastAPI application again, you should see the list of questions at `http://localhost:8000/questions`! 🎉

## Conclusion

In this guide, we learned how to use Django's ORM with FastAPI. This can be extremely useful when migrating from Django to FastAPI, as you can reuse your existing Django models and queries.

## Using the ORM in async routes

Django's support for async is currently limited, if you need to do run any query in an async route (or function),
you need to either use the async equivalent of the query or use `sync_to_async` from `asgiref.sync` to run the query:

//// tab | Python 3.8+

```Python
{!> ../../../docs_src/django_orm/tutorial001.py[ln:23-37]!}
```
