import pytest
from fastapi import FastAPI
from fastapi.params import Body, Depends, Param, ParamTypes


@pytest.fixture(scope="class")
def depends():
    return Depends()


@pytest.fixture(scope="class")
def depends_args():
    return Depends(False, use_cache=False)


@pytest.fixture(scope="class")
def body():
    return Body(1)


@pytest.fixture(scope="class")
def param():
    return Param(1)


@pytest.fixture(scope="class", params=["query", "header", "path", "cookie"])
def param_type(request):
    return ParamTypes(request.param), request.param


class TestParams:
    def test_depends_repr_empty(self, depends):
        assert repr(depends) == "Depends(NoneType)"

    def test_depends_repr_args(self, depends_args):
        assert repr(depends_args) == "Depends(bool, use_cache=False)"

    def test_body_repr(self, body):
        assert repr(body) == "Body(1)"

    def test_param_repr(self, param):
        assert repr(param) == "Param(1)"

    def test_paramtype_repr(self, param_type):
        assert repr(param_type[0]) == "ParamTypes(" + param_type[1] + ")"
