"""
Static file serving for FastAPI.

Re-exports Starlette's StaticFiles class for serving static files
(CSS, JavaScript, images) in FastAPI applications.
"""

from starlette.staticfiles import StaticFiles as StaticFiles  # noqa
