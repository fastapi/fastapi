import warnings

import pytest
from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient


class ResponseLevel0(JSONResponse):
    media_type = "application/x-level-0"


class ResponseLevel1(JSONResponse):
    media_type = "application/x-level-1"


class ResponseLevel2(JSONResponse):
    media_type = "application/x-level-2"


class ResponseLevel3(JSONResponse):
    media_type = "application/x-level-3"


class ResponseLevel4(JSONResponse):
    media_type = "application/x-level-4"


class ResponseLevel5(JSONResponse):
    media_type = "application/x-level-5"


async def dep0(response: Response):
    response.headers["x-level0"] = "True"


async def dep1(response: Response):
    response.headers["x-level1"] = "True"


async def dep2(response: Response):
    response.headers["x-level2"] = "True"


async def dep3(response: Response):
    response.headers["x-level3"] = "True"


async def dep4(response: Response):
    response.headers["x-level4"] = "True"


async def dep5(response: Response):
    response.headers["x-level5"] = "True"


callback_router0 = APIRouter()


@callback_router0.get("/")
async def callback0(level0: str):
    pass  # pragma: nocover


callback_router1 = APIRouter()


@callback_router1.get("/")
async def callback1(level1: str):
    pass  # pragma: nocover


callback_router2 = APIRouter()


@callback_router2.get("/")
async def callback2(level2: str):
    pass  # pragma: nocover


callback_router3 = APIRouter()


@callback_router3.get("/")
async def callback3(level3: str):
    pass  # pragma: nocover


callback_router4 = APIRouter()


@callback_router4.get("/")
async def callback4(level4: str):
    pass  # pragma: nocover


callback_router5 = APIRouter()


@callback_router5.get("/")
async def callback5(level5: str):
    pass  # pragma: nocover


app = FastAPI(
    dependencies=[Depends(dep0)],
    responses={
        400: {"description": "Client error level 0"},
        500: {"description": "Server error level 0"},
    },
    default_response_class=ResponseLevel0,
    callbacks=callback_router0.routes,
)

router2_override = APIRouter(
    prefix="/level2",
    tags=["level2a", "level2b"],
    dependencies=[Depends(dep2)],
    responses={
        402: {"description": "Client error level 2"},
        502: {"description": "Server error level 2"},
    },
    default_response_class=ResponseLevel2,
    callbacks=callback_router2.routes,
    deprecated=True,
)
router2_default = APIRouter()
router4_override = APIRouter(
    prefix="/level4",
    tags=["level4a", "level4b"],
    dependencies=[Depends(dep4)],
    responses={
        404: {"description": "Client error level 4"},
        504: {"description": "Server error level 4"},
    },
    default_response_class=ResponseLevel4,
    callbacks=callback_router4.routes,
    deprecated=True,
)
router4_default = APIRouter()


@app.get(
    "/override1",
    tags=["path1a", "path1b"],
    responses={
        401: {"description": "Client error level 1"},
        501: {"description": "Server error level 1"},
    },
    deprecated=True,
    callbacks=callback_router1.routes,
    dependencies=[Depends(dep1)],
    response_class=ResponseLevel1,
)
async def path1_override(level1: str):
    return level1


@app.get("/default1")
async def path1_default(level1: str):
    return level1


@router2_override.get(
    "/override3",
    tags=["path3a", "path3b"],
    responses={
        403: {"description": "Client error level 3"},
        503: {"description": "Server error level 3"},
    },
    deprecated=True,
    callbacks=callback_router3.routes,
    dependencies=[Depends(dep3)],
    response_class=ResponseLevel3,
)
async def path3_override_router2_override(level3: str):
    return level3


@router2_override.get("/default3")
async def path3_default_router2_override(level3: str):
    return level3


@router2_default.get(
    "/override3",
    tags=["path3a", "path3b"],
    responses={
        403: {"description": "Client error level 3"},
        503: {"description": "Server error level 3"},
    },
    deprecated=True,
    callbacks=callback_router3.routes,
    dependencies=[Depends(dep3)],
    response_class=ResponseLevel3,
)
async def path3_override_router2_default(level3: str):
    return level3


@router2_default.get("/default3")
async def path3_default_router2_default(level3: str):
    return level3


@router4_override.get(
    "/override5",
    tags=["path5a", "path5b"],
    responses={
        405: {"description": "Client error level 5"},
        505: {"description": "Server error level 5"},
    },
    deprecated=True,
    callbacks=callback_router5.routes,
    dependencies=[Depends(dep5)],
    response_class=ResponseLevel5,
)
async def path5_override_router4_override(level5: str):
    return level5


@router4_override.get(
    "/default5",
)
async def path5_default_router4_override(level5: str):
    return level5


@router4_default.get(
    "/override5",
    tags=["path5a", "path5b"],
    responses={
        405: {"description": "Client error level 5"},
        505: {"description": "Server error level 5"},
    },
    deprecated=True,
    callbacks=callback_router5.routes,
    dependencies=[Depends(dep5)],
    response_class=ResponseLevel5,
)
async def path5_override_router4_default(level5: str):
    return level5


@router4_default.get(
    "/default5",
)
async def path5_default_router4_default(level5: str):
    return level5


router2_override.include_router(
    router4_override,
    prefix="/level3",
    tags=["level3a", "level3b"],
    dependencies=[Depends(dep3)],
    responses={
        403: {"description": "Client error level 3"},
        503: {"description": "Server error level 3"},
    },
    default_response_class=ResponseLevel3,
    callbacks=callback_router3.routes,
)

router2_override.include_router(
    router4_default,
    prefix="/level3",
    tags=["level3a", "level3b"],
    dependencies=[Depends(dep3)],
    responses={
        403: {"description": "Client error level 3"},
        503: {"description": "Server error level 3"},
    },
    default_response_class=ResponseLevel3,
    callbacks=callback_router3.routes,
)

router2_override.include_router(router4_override)

router2_override.include_router(router4_default)

router2_default.include_router(
    router4_override,
    prefix="/level3",
    tags=["level3a", "level3b"],
    dependencies=[Depends(dep3)],
    responses={
        403: {"description": "Client error level 3"},
        503: {"description": "Server error level 3"},
    },
    default_response_class=ResponseLevel3,
    callbacks=callback_router3.routes,
)

router2_default.include_router(
    router4_default,
    prefix="/level3",
    tags=["level3a", "level3b"],
    dependencies=[Depends(dep3)],
    responses={
        403: {"description": "Client error level 3"},
        503: {"description": "Server error level 3"},
    },
    default_response_class=ResponseLevel3,
    callbacks=callback_router3.routes,
)

router2_default.include_router(router4_override)

router2_default.include_router(router4_default)


app.include_router(
    router2_override,
    prefix="/level1",
    tags=["level1a", "level1b"],
    dependencies=[Depends(dep1)],
    responses={
        401: {"description": "Client error level 1"},
        501: {"description": "Server error level 1"},
    },
    default_response_class=ResponseLevel1,
    callbacks=callback_router1.routes,
)

app.include_router(
    router2_default,
    prefix="/level1",
    tags=["level1a", "level1b"],
    dependencies=[Depends(dep1)],
    responses={
        401: {"description": "Client error level 1"},
        501: {"description": "Server error level 1"},
    },
    default_response_class=ResponseLevel1,
    callbacks=callback_router1.routes,
)

app.include_router(router2_override)

app.include_router(router2_default)

client = TestClient(app)


def test_level1_override():
    response = client.get("/override1?level1=foo")
    assert response.json() == "foo"
    assert response.headers["content-type"] == "application/x-level-1"
    assert "x-level0" in response.headers
    assert "x-level1" in response.headers
    assert "x-level2" not in response.headers
    assert "x-level3" not in response.headers
    assert "x-level4" not in response.headers
    assert "x-level5" not in response.headers


def test_level1_default():
    response = client.get("/default1?level1=foo")
    assert response.json() == "foo"
    assert response.headers["content-type"] == "application/x-level-0"
    assert "x-level0" in response.headers
    assert "x-level1" not in response.headers
    assert "x-level2" not in response.headers
    assert "x-level3" not in response.headers
    assert "x-level4" not in response.headers
    assert "x-level5" not in response.headers


@pytest.mark.parametrize("override1", [True, False])
@pytest.mark.parametrize("override2", [True, False])
@pytest.mark.parametrize("override3", [True, False])
def test_paths_level3(override1, override2, override3):
    url = ""
    content_type_level = "0"
    if override1:
        url += "/level1"
        content_type_level = "1"
    if override2:
        url += "/level2"
        content_type_level = "2"
    if override3:
        url += "/override3"
        content_type_level = "3"
    else:
        url += "/default3"
    url += "?level3=foo"
    response = client.get(url)
    assert response.json() == "foo"
    assert (
        response.headers["content-type"] == f"application/x-level-{content_type_level}"
    )
    assert "x-level0" in response.headers
    assert not override1 or "x-level1" in response.headers
    assert not override2 or "x-level2" in response.headers
    assert not override3 or "x-level3" in response.headers


@pytest.mark.parametrize("override1", [True, False])
@pytest.mark.parametrize("override2", [True, False])
@pytest.mark.parametrize("override3", [True, False])
@pytest.mark.parametrize("override4", [True, False])
@pytest.mark.parametrize("override5", [True, False])
def test_paths_level5(override1, override2, override3, override4, override5):
    url = ""
    content_type_level = "0"
    if override1:
        url += "/level1"
        content_type_level = "1"
    if override2:
        url += "/level2"
        content_type_level = "2"
    if override3:
        url += "/level3"
        content_type_level = "3"
    if override4:
        url += "/level4"
        content_type_level = "4"
    if override5:
        url += "/override5"
        content_type_level = "5"
    else:
        url += "/default5"
    url += "?level5=foo"
    response = client.get(url)
    assert response.json() == "foo"
    assert (
        response.headers["content-type"] == f"application/x-level-{content_type_level}"
    )
    assert "x-level0" in response.headers
    assert not override1 or "x-level1" in response.headers
    assert not override2 or "x-level2" in response.headers
    assert not override3 or "x-level3" in response.headers
    assert not override4 or "x-level4" in response.headers
    assert not override5 or "x-level5" in response.headers


def test_openapi():
    client = TestClient(app)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        response = client.get("/openapi.json")
        assert issubclass(w[-1].category, UserWarning)
        assert "Duplicate Operation ID" in str(w[-1].message)
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/override1": {
                "get": {
                    "tags": ["path1a", "path1b"],
                    "summary": "Path1 Override",
                    "operationId": "path1_override_override1_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level1", "type": "string"},
                            "name": "level1",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-1": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/default1": {
                "get": {
                    "summary": "Path1 Default",
                    "operationId": "path1_default_default1_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level1", "type": "string"},
                            "name": "level1",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-0": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    },
                }
            },
            "/level1/level2/override3": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "path3a",
                        "path3b",
                    ],
                    "summary": "Path3 Override Router2 Override",
                    "operationId": "path3_override_router2_override_level1_level2_override3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/default3": {
                "get": {
                    "tags": ["level1a", "level1b", "level2a", "level2b"],
                    "summary": "Path3 Default Router2 Override",
                    "operationId": "path3_default_router2_override_level1_level2_default3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-2": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/level3/level4/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level1_level2_level3_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/level3/level4/default5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                    ],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level1_level2_level3_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/level3/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level1_level2_level3_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/level3/default5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                    ],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level1_level2_level3_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/level4/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level1_level2_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/level4/default5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "level4a",
                        "level4b",
                    ],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level1_level2_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level2a",
                        "level2b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level1_level2_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level2/default5": {
                "get": {
                    "tags": ["level1a", "level1b", "level2a", "level2b"],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level1_level2_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-2": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "402": {"description": "Client error level 2"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "502": {"description": "Server error level 2"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/override3": {
                "get": {
                    "tags": ["level1a", "level1b", "path3a", "path3b"],
                    "summary": "Path3 Override Router2 Default",
                    "operationId": "path3_override_router2_default_level1_override3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/default3": {
                "get": {
                    "tags": ["level1a", "level1b"],
                    "summary": "Path3 Default Router2 Default",
                    "operationId": "path3_default_router2_default_level1_default3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-1": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                }
            },
            "/level1/level3/level4/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level1_level3_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level3/level4/default5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                    ],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level1_level3_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level3/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level3a",
                        "level3b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level1_level3_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "403": {"description": "Client error level 3"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "503": {"description": "Server error level 3"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level3/default5": {
                "get": {
                    "tags": ["level1a", "level1b", "level3a", "level3b"],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level1_level3_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                }
            },
            "/level1/level4/override5": {
                "get": {
                    "tags": [
                        "level1a",
                        "level1b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level1_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/level4/default5": {
                "get": {
                    "tags": ["level1a", "level1b", "level4a", "level4b"],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level1_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/override5": {
                "get": {
                    "tags": ["level1a", "level1b", "path5a", "path5b"],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level1_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level1/default5": {
                "get": {
                    "tags": ["level1a", "level1b"],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level1_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-1": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "401": {"description": "Client error level 1"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "501": {"description": "Server error level 1"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback1": {
                            "/": {
                                "get": {
                                    "summary": "Callback1",
                                    "operationId": "callback1__get",
                                    "parameters": [
                                        {
                                            "name": "level1",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level1",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                }
            },
            "/level2/override3": {
                "get": {
                    "tags": ["level2a", "level2b", "path3a", "path3b"],
                    "summary": "Path3 Override Router2 Override",
                    "operationId": "path3_override_router2_override_level2_override3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/default3": {
                "get": {
                    "tags": ["level2a", "level2b"],
                    "summary": "Path3 Default Router2 Override",
                    "operationId": "path3_default_router2_override_level2_default3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-2": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/level3/level4/override5": {
                "get": {
                    "tags": [
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level2_level3_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/level3/level4/default5": {
                "get": {
                    "tags": [
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                    ],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level2_level3_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/level3/override5": {
                "get": {
                    "tags": [
                        "level2a",
                        "level2b",
                        "level3a",
                        "level3b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level2_level3_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/level3/default5": {
                "get": {
                    "tags": ["level2a", "level2b", "level3a", "level3b"],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level2_level3_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/level4/override5": {
                "get": {
                    "tags": [
                        "level2a",
                        "level2b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level2_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/level4/default5": {
                "get": {
                    "tags": ["level2a", "level2b", "level4a", "level4b"],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level2_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/override5": {
                "get": {
                    "tags": ["level2a", "level2b", "path5a", "path5b"],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level2_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level2/default5": {
                "get": {
                    "tags": ["level2a", "level2b"],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level2_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-2": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "402": {"description": "Client error level 2"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "502": {"description": "Server error level 2"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback2": {
                            "/": {
                                "get": {
                                    "summary": "Callback2",
                                    "operationId": "callback2__get",
                                    "parameters": [
                                        {
                                            "name": "level2",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level2",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/override3": {
                "get": {
                    "tags": ["path3a", "path3b"],
                    "summary": "Path3 Override Router2 Default",
                    "operationId": "path3_override_router2_default_override3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/default3": {
                "get": {
                    "summary": "Path3 Default Router2 Default",
                    "operationId": "path3_default_router2_default_default3_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level3", "type": "string"},
                            "name": "level3",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-0": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    },
                }
            },
            "/level3/level4/override5": {
                "get": {
                    "tags": [
                        "level3a",
                        "level3b",
                        "level4a",
                        "level4b",
                        "path5a",
                        "path5b",
                    ],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level3_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level3/level4/default5": {
                "get": {
                    "tags": ["level3a", "level3b", "level4a", "level4b"],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level3_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "403": {"description": "Client error level 3"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "503": {"description": "Server error level 3"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level3/override5": {
                "get": {
                    "tags": ["level3a", "level3b", "path5a", "path5b"],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_level3_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "403": {"description": "Client error level 3"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "503": {"description": "Server error level 3"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level3/default5": {
                "get": {
                    "tags": ["level3a", "level3b"],
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_level3_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-3": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "403": {"description": "Client error level 3"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "503": {"description": "Server error level 3"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback3": {
                            "/": {
                                "get": {
                                    "summary": "Callback3",
                                    "operationId": "callback3__get",
                                    "parameters": [
                                        {
                                            "name": "level3",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level3",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                }
            },
            "/level4/override5": {
                "get": {
                    "tags": ["level4a", "level4b", "path5a", "path5b"],
                    "summary": "Path5 Override Router4 Override",
                    "operationId": "path5_override_router4_override_level4_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "404": {"description": "Client error level 4"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "504": {"description": "Server error level 4"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/level4/default5": {
                "get": {
                    "tags": ["level4a", "level4b"],
                    "summary": "Path5 Default Router4 Override",
                    "operationId": "path5_default_router4_override_level4_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-4": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "404": {"description": "Client error level 4"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "504": {"description": "Server error level 4"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback4": {
                            "/": {
                                "get": {
                                    "summary": "Callback4",
                                    "operationId": "callback4__get",
                                    "parameters": [
                                        {
                                            "name": "level4",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level4",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/override5": {
                "get": {
                    "tags": ["path5a", "path5b"],
                    "summary": "Path5 Override Router4 Default",
                    "operationId": "path5_override_router4_default_override5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-5": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "405": {"description": "Client error level 5"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                        "505": {"description": "Server error level 5"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                        "callback5": {
                            "/": {
                                "get": {
                                    "summary": "Callback5",
                                    "operationId": "callback5__get",
                                    "parameters": [
                                        {
                                            "name": "level5",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level5",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "deprecated": True,
                }
            },
            "/default5": {
                "get": {
                    "summary": "Path5 Default Router4 Default",
                    "operationId": "path5_default_router4_default_default5_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Level5", "type": "string"},
                            "name": "level5",
                            "in": "query",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/x-level-0": {"schema": {}}},
                        },
                        "400": {"description": "Client error level 0"},
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                        "500": {"description": "Server error level 0"},
                    },
                    "callbacks": {
                        "callback0": {
                            "/": {
                                "get": {
                                    "summary": "Callback0",
                                    "operationId": "callback0__get",
                                    "parameters": [
                                        {
                                            "name": "level0",
                                            "in": "query",
                                            "required": True,
                                            "schema": {
                                                "title": "Level0",
                                                "type": "string",
                                            },
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful Response",
                                            "content": {
                                                "application/json": {"schema": {}}
                                            },
                                        },
                                        "422": {
                                            "description": "Validation Error",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "$ref": "#/components/schemas/HTTPValidationError"
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
            }
        },
    }
