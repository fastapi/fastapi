from importlib import import_module

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY


def create_authenticated_session(user):
    """Creates an authenticated session for the given user."""

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session.create()

    session[SESSION_KEY] = str(user.id)
    session[BACKEND_SESSION_KEY] = (
        user.backend
        if hasattr(user, "backend")
        else "django.contrib.auth.backends.ModelBackend"
    )
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()

    session.save()

    return session.session_key
