import pytest
from fastapi import UploadFile
from fastapi.datastructures import Default


def test_upload_file_invalid():
    with pytest.raises(ValueError):
        UploadFile.validate("not a Starlette UploadFile")


def test_default_placeholder_equals():
    placeholder_1 = Default("a")
    placeholder_2 = Default("a")
    assert placeholder_1 == placeholder_2
    assert placeholder_1.value == placeholder_2.value


def test_default_placeholder_bool():
    placeholder_a = Default("a")
    placeholder_b = Default("")
    assert placeholder_a
    assert not placeholder_b
