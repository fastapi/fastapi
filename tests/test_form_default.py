from typing import Any, List, Optional

import pytest
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .utils import needs_pydanticv2


class FormParams(BaseModel):
    param_1: str = "default"
    param_2: Annotated[str, Field(alias="param_2_alias")] = "default"
    param_3: Annotated[str, Form(alias="param_3_alias")] = "default"
    upload_file: Optional[UploadFile] = None
    file: Annotated[Optional[bytes], File()] = None


app = FastAPI()


@app.post("/form-param")
def form_param(
    param_1: Annotated[str, Form()] = "default",
    param_2: Annotated[str, Form(alias="param_2_alias")] = "default",
    upload_file: Optional[UploadFile] = None,
    file: Annotated[Optional[bytes], File()] = None,
):
    return {
        "param_1": param_1,
        "param_2": param_2,
        "upload_file": upload_file,
        "file": file,
    }


@app.post("/form-model")
def form_model(params: Annotated[FormParams, Form()]):
    return {
        "param_1": params.param_1,
        "param_2": params.param_2,
        "param_3": params.param_3,
        "upload_file": params.upload_file,
        "file": params.file,
    }


@app.post("/form-param-list-with-default")
def form_param_list_with_default(
    params: Annotated[
        List[str],
        Form(),
    ] = [],  # noqa: B006 (default_factory doesn't work with Pydantic V1)
):
    return {"params": params}


@app.post("/form-param-optional-list")
def form_param_optional_list(
    params: Annotated[Optional[List[str]], Form()] = None,
):
    return {"params": params}


@app.post("/form-model-fields-set")
def form_model_fields_set(params: Annotated[FormParams, Form()]):
    return {"fields_set": params.model_fields_set}


# ====================================================================================
# Tests


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="no_data_sent"),
        pytest.param(
            {"param_1": "", "param_2_alias": "", "upload_file": "", "file": ""},
            id="empty_strings_sent",
        ),
    ],
)
def test_defaults_form_param(client: TestClient, data: dict):
    """
    Empty string or no input data - default value is used.
    For parameters declared as single Form fields.
    """
    response = client.post("/form-param", data=data)
    assert response.json() == {
        "param_1": "default",
        "param_2": "default",
        "upload_file": None,
        "file": None,
    }


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="no_data_sent"),
        pytest.param(
            {
                "param_1": "",
                "param_2_alias": "",
                "param_3_alias": "",
                "upload_file": "",
                "file": "",
            },
            id="empty_strings_sent",
        ),
    ],
)
def test_defaults_form_model(client: TestClient, data: dict):
    """
    Empty string or no data - default value is used.
    For parameters declared as Form model.
    """
    response = client.post("/form-model", data=data)
    assert response.json() == {
        "param_1": "default",
        "param_2": "default",
        "param_3": "default",
        "upload_file": None,
        "file": None,
    }


@pytest.mark.parametrize(
    ("url", "expected_res"),
    [
        ("/form-param-list-with-default", []),
        ("/form-param-optional-list", None),
    ],
)
def test_form_list_param_no_input(client: TestClient, url: str, expected_res: Any):
    """
    No input data passed to list parameter - default value is used.
    """
    response = client.post(url)
    assert response.json() == {"params": expected_res}


@pytest.mark.parametrize(
    ("data", "expected_res"),
    [
        ({"params": ""}, [""]),
        ({"params": [""]}, [""]),
        ({"params": ["", "a"]}, ["", "a"]),
        ({"params": ["a", ""]}, ["a", ""]),
    ],
)
@pytest.mark.parametrize(
    "url", ["/form-param-list-with-default", "/form-param-optional-list"]
)
def test_form_list_param_empty_str(
    client: TestClient, url: str, data: dict, expected_res: Any
):
    """
    Empty strings passed to list parameter treated as empty strings.
    """
    response = client.post(url, data=data)
    assert response.json() == {"params": expected_res}


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="no_data_sent"),
        pytest.param(
            {
                "param_1": "",
                "param_2_alias": "",
                "param_3_alias": "",
                "upload_file": "",
                "file": "",
            },
            id="empty_strings_sent",
        ),
    ],
)
@needs_pydanticv2
def test_form_model_fields_set(client: TestClient, data: dict):
    """
    Check that fields are not pre-populated with default values when no data sent or
    empty string sent.
    """
    response = client.post("/form-model-fields-set", data=data)
    assert response.json() == {"fields_set": []}
