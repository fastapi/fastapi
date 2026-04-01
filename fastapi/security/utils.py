def get_authorization_scheme_param(
    authorization_header_value: str | None,
) -> tuple[str, str]:
    """
    Parse an ``Authorization`` header value into its scheme and parameter.

    Returns a tuple of ``(scheme, credentials)``. If the header is ``None``
    or empty, returns ``("", "")``.
    """
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param.strip()
