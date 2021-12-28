from typing import Optional

from fastapi import FastAPI, Body, Header, Depends, extra_parameters
from fastapi.signature_extensions import exclude_parameters
from fastapi.testclient import TestClient

from pydantic import BaseModel


class Schema_1(BaseModel):
    schema_1_param_1: int
    schema_1_param_2: str


async def dependency_1(dependency_1_param_1: int = 1, dependency_1_param_2: int = 2):
    return {
        "dependency_1_param_1": dependency_1_param_1,
        "dependency_1_param_2": dependency_1_param_2
    }


openapi_schema =  {
    'components': {
        'schemas': {
            'HTTPValidationError': {
                'properties': {
                    'detail': {
                        'items': {
                            '$ref': '#/components/schemas/ValidationError'
                        },
                        'title': 'Detail',
                        'type': 'array'
                    }
                },
                'title': 'HTTPValidationError',
                'type': 'object'
            },
            'ValidationError': {
                'properties': {
                    'loc': {
                        'items': {
                            'type': 'string'
                        },
                        'title': 'Location',
                        'type': 'array'
                    },
                    'msg': {
                        'title': 'Message',
                        'type': 'string'
                    },
                    'type': {
                        'title': 'Error Type',
                        'type': 'string'
                    }
                },
                'required': [
                    'loc',
                    'msg',
                    'type'
                ],
                'title': 'ValidationError',
                'type': 'object'
            },
            'Schema_1': {
                'properties': {
                    'schema_1_param_1': {
                        'title': 'Schema 1 Param 1',
                        'type': 'integer'
                    },
                    'schema_1_param_2': {
                        'title': 'Schema 1 Param 2',
                        'type': 'string'
                    }
                },
                'required': [
                    'schema_1_param_1',
                    'schema_1_param_2'
                ],
                'title': 'Schema_1',
                'type': 'object'
            },
            'Body_endpoint_1_test_1_get': {
                'properties': {
                    'extra_param_schema_1': {
                        '$ref': '#/components/schemas/Schema_1'
                    },
                    'extra_param_body': {
                        'default': 'aaa',
                        'title': 'Extra Param Body',
                        'type': 'string'
                    }
                },
                'required': [
                    'extra_param_schema_1',
                ],
                'title': 'Body_endpoint_1_test_1_get',
                'type': 'object'
            },
        }
    },
    'info': {
        'title': 'FastAPI',
        'version': '0.1.0'
    },
    'openapi': '3.0.2',
    'paths': {
        '/test_1': {
            'get': {
                'operationId': 'endpoint_1_test_1_get',
                'parameters': [
                    {
                        'in': 'query',
                        'name': 'func_param_1',
                        'required': True,
                        'schema': {
                            'title': 'Func Param 1'
                        }
                    },
                    {
                        'in': 'query',
                        'name': 'extra_param_str',
                        'required': True,
                        'schema': {
                            'title': 'Extra Param Str',
                            'type': 'string'
                        }
                    },
                    {
                        'in': 'query',
                        'name': 'extra_param_str_default',
                        'required': False,
                        'schema': {
                            'default': 'aaa',
                            'title': 'Extra Param Str Default',
                            'type': 'string'
                        }
                    },
                    {
                        'in': 'query',
                        'name': 'dependency_1_param_1',
                        'required': False,
                        'schema': {
                            'default': 1,
                            'title': 'Dependency 1 Param 1',
                            'type': 'integer'
                        }
                    },
                    {
                        'in': 'query',
                        'name': 'dependency_1_param_2',
                        'required': False,
                        'schema': {
                            'default': 2,
                            'title': 'Dependency 1 Param 2',
                            'type': 'integer'
                        }
                    },
                    {
                        'in': 'header',
                        'name': 'extra-param-header',
                        'required': False,
                        'schema': {
                            'default': 'aaa',
                            'title': 'Extra-Param-Header',
                            'type': 'string'
                        }
                    }
                ],
                'requestBody': {
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/Body_endpoint_1_test_1_get'
                            }
                        }
                    },
                    'required': True
                },
                'responses': {
                    '200': {
                        'content': {
                            'application/json': {
                                'schema': {}
                            }
                        },
                        'description': 'Successful Response'
                    },
                    '422': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/HTTPValidationError'
                                }
                            }
                        },
                        'description': 'Validation Error'
                    }
                },
                'summary': 'Endpoint 1'
            }
        },
    }
}


app = FastAPI()


@app.get("/test_1")
@extra_parameters(
    extra_param_str=str,
    extra_param_str_default=(str, 'aaa'),
    extra_param_schema_1=Schema_1,
    extra_param_body=(str, Body('aaa')),
    extra_param_header=(str, Header('aaa')),
    extra_param_depends=(dict, Depends(dependency_1)),
)
@exclude_parameters("excluded_param")
def endpoint_1(func_param_1, extra_param_str, excluded_param: int = 1, **kwargs):
    return {}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema
