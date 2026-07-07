"""RFC 9457 Problem Details for HTTP APIs."""

import http.client
from collections.abc import Mapping, Sequence
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


class ProblemDetails(BaseModel):
    type: str = "about:blank"
    title: str | None = None
    status: int | None = None
    detail: str | None = None
    instance: str | None = None

    model_config = ConfigDict(extra="allow")


def _slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("'", "")


def resolve_problem_type(
    *,
    explicit_type: str | None = None,
    status_code: int | None = None,
    error_kind: str | None = None,
    type_base_uri: str | None = None,
    problem_types: Mapping[int | type, str] | None = None,
) -> str:
    segment: str | None = None

    if explicit_type:
        segment = explicit_type
    elif problem_types and status_code is not None:
        segment = problem_types.get(status_code)

    if segment is not None:
        if segment.startswith(("http://", "https://", "about:", "tag:", "urn:")):
            return segment
        if type_base_uri:
            return f"{type_base_uri.rstrip('/')}/{segment.lstrip('/')}"
        return segment

    if error_kind:
        if type_base_uri:
            return f"{type_base_uri.rstrip('/')}/{error_kind}"
        return error_kind

    if type_base_uri and status_code is not None:
        reason = http.client.responses.get(status_code)
        if reason:
            segment = _slugify(reason)
            return f"{type_base_uri.rstrip('/')}/{segment}"

    return "about:blank"


def problem_details_from_http_exception(
    exc: Any,
    *,
    url: str | None = None,
    type_base_uri: str | None = None,
    problem_types: Mapping[int | type, str] | None = None,
) -> ProblemDetails:
    status_code: int = exc.status_code
    detail: Any = getattr(exc, "detail", None)
    detail_str = detail if isinstance(detail, str) else None
    kwargs: dict[str, Any] = {}
    if not isinstance(detail, str) and detail is not None:
        kwargs["errors"] = jsonable_encoder(detail)
    problem_type = resolve_problem_type(
        explicit_type=getattr(exc, "type", None),
        status_code=status_code,
        type_base_uri=type_base_uri,
        problem_types=problem_types,
    )
    return ProblemDetails(
        type=problem_type,
        title=http.client.responses.get(status_code),
        status=status_code,
        detail=detail_str,
        instance=url,
        **kwargs,
    )


def problem_details_from_request_validation(
    errors: Sequence[Any],
    *,
    url: str | None = None,
    type_base_uri: str | None = None,
    problem_types: Mapping[int | type, str] | None = None,
) -> ProblemDetails:
    errors_list = list(errors)
    num_errors = len(errors_list)
    problem_type = resolve_problem_type(
        status_code=422,
        error_kind="validation-error",
        type_base_uri=type_base_uri,
        problem_types=problem_types,
    )
    extra: dict[str, Any] = {"errors": jsonable_encoder(errors_list)}
    return ProblemDetails(
        type=problem_type,
        title="Validation Error",
        status=422,
        detail=f"{num_errors} validation error{'s' if num_errors != 1 else ''}",
        instance=url,
        **extra,
    )
