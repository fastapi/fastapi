# Use Old 403 Authentication Error Status Codes { #use-old-403-authentication-error-status-codes }

Before FastAPI version `0.122.0`, when the integrated security utilities returned an error to the client after a failed authentication, they used the HTTP status code `403 Forbidden`.

Starting with FastAPI version `0.122.0`, they use the more appropriate HTTP status code `401 Unauthorized`, and return a sensible `WWW-Authenticate` header in the response, following the HTTP specifications, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

But if for some reason your clients depend on the old behavior, you can revert to it by overriding the method `make_not_authenticated_error` in your security classes.

For example, you can create a subclass of `HTTPBearer` that returns a `403 Forbidden` error instead of the default `401 Unauthorized` error:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip

Notice that the function returns the exception instance, it doesn't raise it. The raising is done in the rest of the internal code.

///
