import inspect

import pytest
from fastapi import APIRouter, FastAPI


@pytest.mark.parametrize(
    "method_name", ["get", "put", "post", "delete", "options", "head", "patch", "trace"]
)
@pytest.mark.parametrize(
    "sig_param", inspect.signature(APIRouter.get).parameters.items()
)
def test_signatures_consistency(method_name, sig_param):
    router_method = getattr(APIRouter, method_name)
    app_method = getattr(FastAPI, method_name)
    router_sig = inspect.signature(router_method)
    app_sig = inspect.signature(app_method)
    param: inspect.Parameter
    key, param = sig_param
    router_param: inspect.Parameter = router_sig.parameters[key]
    app_param: inspect.Parameter = app_sig.parameters[key]
    assert param.annotation == router_param.annotation
    assert param.annotation == app_param.annotation
    assert param.default == router_param.default
    assert param.default == app_param.default
