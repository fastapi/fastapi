from contextvars import ContextVar
from typing import Annotated

from django.core.asgi import ASGIHandler
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from fastapi import Depends, Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

_django_request = ContextVar[HttpRequest | None]("fastapi_django_request", default=None)


def get_django_request():
    django_request = _django_request.get()

    if not django_request:
        raise ValueError(
            "Django Request not found, did you forget to add the Django Middleware?"
        )

    return django_request


DjangoRequestDep = Annotated[HttpRequest, Depends(get_django_request)]


class DjangoMiddleware(BaseHTTPMiddleware, ASGIHandler):
    """A FastAPI Middleware that runs the Django HTTP Request lifecycle.

    This middleware is responsible for running the Django HTTP Request lifecycle
    in the FastAPI application. It is useful when you want to use Django's
    authentication system, or any other Django feature that requires the
    Django Request object to be available."""

    def __init__(self, *args, **kwargs):
        ASGIHandler.__init__(self)

        super().__init__(*args, **kwargs)

    async def _get_response_async(self, request):
        fastapi_response = await self._call_next(request)

        assert isinstance(fastapi_response, StreamingResponse)

        return StreamingHttpResponse(
            streaming_content=fastapi_response.body_iterator,
            headers=fastapi_response.headers,
            status=fastapi_response.status_code,
        )

    async def __call__(self, scope, receive, send):
        self._django_request, _ = self.create_request(scope, "")

        _django_request.set(self._django_request)

        await BaseHTTPMiddleware.__call__(self, scope, receive, send)

    async def dispatch(self, request: Request, call_next):
        self._call_next = call_next

        django_response = await self.get_response_async(self._django_request)

        if isinstance(django_response, HttpResponse):
            return Response(
                status_code=django_response.status_code,
                content=django_response.content,
                headers=django_response.headers,
            )

        if isinstance(django_response, StreamingHttpResponse):

            async def streaming():
                async for chunk in django_response.streaming_content:
                    yield chunk

            return StreamingResponse(
                status_code=django_response.status_code,
                content=streaming(),
                headers=django_response.headers,
            )

        return Response(status_code=500)
