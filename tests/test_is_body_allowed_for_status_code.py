import pytest
from fastapi.utils import is_body_allowed_for_status_code


@pytest.mark.parametrize(
    "status_code",
    [
        None,
        "default",
        "1XX",
        "2XX",
        "3XX",
        "4XX",
        "5XX",
    ],
)
def test_allows_body_for_patterned_and_unset_status_codes(
    status_code: str | None,
) -> None:
    # Ref: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#patterned-fields-1
    assert is_body_allowed_for_status_code(status_code)


@pytest.mark.parametrize(
    "status_code",
    [
        100,
        199,
        "100",
        "199",
        204,
        205,
        304,
        "204",
        "205",
        "304",
    ],
)
def test_disallows_body_for_empty_content_status_codes(status_code: int | str) -> None:
    assert not is_body_allowed_for_status_code(status_code)


@pytest.mark.parametrize(
    "status_code",
    [
        200,
        201,
        300,
        301,
        302,
        400,
        404,
        500,
        "200",
        "302",
        "404",
        "500",
    ],
)
def test_allows_body_for_regular_status_codes(status_code: int | str) -> None:
    assert is_body_allowed_for_status_code(status_code)
