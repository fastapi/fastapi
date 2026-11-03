import pytest

from fastapi.encoders import jsonable_encoder


def test_a_single_callable_as_custom_encoder_is_named():
    with pytest.raises(TypeError, match="custom_encoder must be a mapping"):
        jsonable_encoder({"a": 1}, custom_encoder=str)


def test_a_mapping_of_encoders_still_works():
    class Custom:
        pass

    encoded = jsonable_encoder(
        {"item": Custom()},
        custom_encoder={Custom: lambda value: "custom"},
    )

    assert encoded == {"item": "custom"}


def test_no_custom_encoder_behaves_as_before():
    assert jsonable_encoder({"a": 1}) == {"a": 1}
