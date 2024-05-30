import functools
import http.cookies
import secrets
from re import Pattern
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, cast

from itsdangerous import BadSignature
from itsdangerous.url_safe import URLSafeSerializer
from starlette.datastructures import URL, MutableHeaders
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class CSRFMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        secret: str,
        *,
        required_urls: Optional[List[Pattern]] = None,
        exempt_urls: Optional[List[Pattern]] = None,
        sensitive_cookies: Optional[Set[str]] = None,
        safe_methods: Optional[Set[str]] = None,
        cookie_name: str = "csrftoken",
        cookie_path: str = "/",
        cookie_domain: Optional[str] = None,
        cookie_secure: bool = False,
        cookie_httponly: bool = False,
        cookie_samesite: str = "lax",
        header_name: str = "x-csrftoken",
    ) -> None:
        self.app = app
        self.serializer = URLSafeSerializer(secret, "csrftoken")
        self.secret = secret
        self.required_urls = required_urls
        self.exempt_urls = exempt_urls
        self.sensitive_cookies = sensitive_cookies
        if safe_methods is None:
            self.safe_methods = {"GET", "HEAD", "OPTIONS", "TRACE"}
        self.cookie_name = cookie_name
        self.cookie_path = cookie_path
        self.cookie_domain = cookie_domain
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        self.cookie_samesite = cookie_samesite
        self.header_name = header_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        body = await self._get_request_body(request)
        csrf_cookie = request.cookies.get(self.cookie_name)

        if self._url_is_required(request.url) or (
            request.method not in self.safe_methods
            and not self._url_is_exempt(request.url)
            and self._has_sensitive_cookies(request.cookies)
        ):
            submitted_csrf_token = await self._get_submitted_csrf_token(request)

            if (
                not csrf_cookie
                or not submitted_csrf_token
                or not self._csrf_tokens_match(csrf_cookie, submitted_csrf_token)
            ):
                response = self._get_error_response(request)
                await response(scope, receive, send)
                return

        request._receive = self._receive_with_body(request._receive, body)
        send = functools.partial(self.send, send=send, scope=scope)
        await self.app(scope, request.receive, send)

    async def send(self, message: Message, send: Send, scope: Scope) -> None:
        request = Request(scope)
        csrf_cookie = request.cookies.get(self.cookie_name)

        if csrf_cookie is None:
            message.setdefault("headers", [])
            headers = MutableHeaders(scope=message)
            cookie: http.cookies.BaseCookie = http.cookies.SimpleCookie()
            cookie_name = self.cookie_name
            cookie[cookie_name] = self._generate_csrf_token()
            cookie[cookie_name]["path"] = self.cookie_path
            cookie[cookie_name]["secure"] = self.cookie_secure
            cookie[cookie_name]["httponly"] = self.cookie_httponly
            cookie[cookie_name]["samesite"] = self.cookie_samesite
            if self.cookie_domain is not None:
                cookie[cookie_name]["domain"] = self.cookie_domain  # pragma: no cover
            headers.append("set-cookie", cookie.output(header="").strip())

        await send(message)

    def _has_sensitive_cookies(self, cookies: Dict[str, str]) -> bool:
        if not self.sensitive_cookies:
            return True
        for sensitive_cookie in self.sensitive_cookies:
            if sensitive_cookie in cookies:
                return True
        return False

    def _url_is_required(self, url: URL) -> bool:
        if not self.required_urls:
            return False
        for required_url in self.required_urls:
            if required_url.match(url.path):
                return True
        return False

    def _url_is_exempt(self, url: URL) -> bool:
        if not self.exempt_urls:
            return False
        for exempt_url in self.exempt_urls:
            if exempt_url.match(url.path):
                return True
        return False

    async def _get_request_body(self, request: Request):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return await request.body()
        return b""

    async def _get_submitted_csrf_token(self, request: Request) -> Optional[str]:
        csrf_token_header = request.headers.get(self.header_name)
        if csrf_token_header:
            return csrf_token_header
        csrftoken_form = await self._get_csrf_token_form(request)
        return csrftoken_form

    async def _get_csrf_token_form(self, request: Request) -> str:
        form = await request.form()
        csrf_token = form.get(self.cookie_name, "")
        return cast(str, csrf_token)

    def _generate_csrf_token(self) -> str:
        token = self.serializer.dumps(secrets.token_urlsafe(128))
        return cast(str, token)

    def _csrf_tokens_match(self, token1: str, token2: str) -> bool:
        try:
            decoded1: str = self.serializer.loads(token1)
            decoded2: str = self.serializer.loads(token2)
            return secrets.compare_digest(decoded1, decoded2)
        except BadSignature:
            return False

    def _get_error_response(self, request: Request) -> Response:
        return PlainTextResponse(
            content="CSRF token verification failed", status_code=403
        )

    def _receive_with_body(
        self, receive: Any, body: bytes
    ) -> Callable[[], Coroutine[Any, Any, Dict[str, Any]]]:
        async def inner() -> dict:
            return {"type": "http.request", "body": body, "more_body": False}

        return inner


def csrf_token_processor(csrf_cookie_name: str, csrf_header_name: str):
    def processor(request: Request) -> Dict[str, Any]:
        csrf_token = request.cookies.get(csrf_cookie_name)
        csrf_input = (
            f'<input type="hidden" name="{csrf_cookie_name}" value="{csrf_token}">'
        )
        csrf_header = {csrf_header_name: csrf_token}
        return {
            "csrf_token": csrf_token,
            "csrf_input": csrf_input,
            "csrf_header": csrf_header,
        }

    return processor
