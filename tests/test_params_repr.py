import pytest
from fastapi import FastAPI
from fastapi.params import Body, Depends


@pytest.fixture(scope="class")
def depends():
    return Depends()


@pytest.fixture(scope="class")
def depends_args():
    return Depends(False, use_cache=False)


@pytest.fixture(scope="class")
def body():
    return Body(1)


class TestParams:
    def test_depends_repr_empty(self, depends):
        assert repr(depends) == "Depends(NoneType)"

    def test_depends_repr_args(self, depends_args):
        assert repr(depends_args) == "Depends(bool, use_cache=False)"

    def test_body_repr(self, body):
        assert repr(body) == "Body(1)"
