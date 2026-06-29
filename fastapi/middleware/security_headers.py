from starlette.types import ASGIApp, Message, Receive, Scope, Send


class SecurityHeadersMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        *,
        hsts: bool | str = True,
        x_content_type_options: str | None = "nosniff",
        x_frame_options: str | None = "DENY",
        referrer_policy: str | None = "strict-origin-when-cross-origin",
        cross_origin_opener_policy: str | None = "same-origin",
        content_security_policy: str | None = None,
        permissions_policy: str | None = None,
        cross_origin_embedder_policy: str | None = None,
        cross_origin_resource_policy: str | None = None,
        cache_control: str | None = None,
    ) -> None:
        self.app = app
        self._headers: dict[bytes, bytes] = {}

        if hsts is True:
            self._headers[b"strict-transport-security"] = (
                b"max-age=31536000; includeSubDomains"
            )
        elif isinstance(hsts, str):
            self._headers[b"strict-transport-security"] = hsts.encode("latin-1")

        if x_content_type_options is not None:
            self._headers[b"x-content-type-options"] = x_content_type_options.encode(
                "latin-1"
            )
        if x_frame_options is not None:
            self._headers[b"x-frame-options"] = x_frame_options.encode("latin-1")
        if referrer_policy is not None:
            self._headers[b"referrer-policy"] = referrer_policy.encode("latin-1")
        if cross_origin_opener_policy is not None:
            self._headers[b"cross-origin-opener-policy"] = (
                cross_origin_opener_policy.encode("latin-1")
            )
        if content_security_policy is not None:
            self._headers[b"content-security-policy"] = content_security_policy.encode(
                "latin-1"
            )
        if permissions_policy is not None:
            self._headers[b"permissions-policy"] = permissions_policy.encode("latin-1")
        if cross_origin_embedder_policy is not None:
            self._headers[b"cross-origin-embedder-policy"] = (
                cross_origin_embedder_policy.encode("latin-1")
            )
        if cross_origin_resource_policy is not None:
            self._headers[b"cross-origin-resource-policy"] = (
                cross_origin_resource_policy.encode("latin-1")
            )
        if cache_control is not None:
            self._headers[b"cache-control"] = cache_control.encode("latin-1")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                existing = {k.lower(): k for k, _ in message["headers"]}
                headers = list(message["headers"])
                for header_name, header_value in self._headers.items():
                    if header_name not in existing:
                        headers.append((header_name, header_value))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)
