from typing import Optional


def get_authorization_scheme_param(
    authorization_header_value: Optional[str],
) -> tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param.strip()
