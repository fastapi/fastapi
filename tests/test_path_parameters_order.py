from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI()


async def check_current_user(request: Request, user_id: str):
    # Imagine, there's a check that user exists
    request.state.current_user_id = user_id


async def check_current_project(request: Request, project_id: str):
    # Imagine, there's a check that project exists
    request.state.current_project_id = project_id


async def current_user(request: Request):
    return request.state.current_user_id


async def current_project(request: Request):
    return request.state.current_project_id


router_users = APIRouter(prefix="/users")

router_projects = APIRouter(
    prefix="/{user_id}/projects",
    dependencies=[Depends(check_current_user)],
)

router_issues = APIRouter(
    prefix="/{project_id}/issues",
    dependencies=[Depends(check_current_project)],
)


@router_issues.get("/{issue_id}")
async def get_issue(
    issue_id: str,
    current_user: str = Depends(current_user),
    current_project: str = Depends(current_project),
):
    return {
        "user_id": current_user,
        "project_id": current_project,
        "issue_id": issue_id,
    }


router_projects.include_router(router_issues)
router_users.include_router(router_projects)
app.include_router(router_users)


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/{user_id}/projects/{project_id}/issues/{issue_id}": {
            "get": {
                "summary": "Get Issue",
                "operationId": "get_issue_users__user_id__projects__project_id__issues__issue_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "User Id", "type": "string"},
                        "name": "user_id",
                        "in": "path",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Project Id", "type": "string"},
                        "name": "project_id",
                        "in": "path",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Issue Id", "type": "string"},
                        "name": "issue_id",
                        "in": "path",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
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
                            "anyOf": [
                                {"type": "string"},
                                {"type": "integer"},
                            ]
                        },
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_path_parameters_order_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_path_parameters_order_get():

    path_params = {
        "user_id": "1",
        "project_id": "2",
        "issue_id": "3",
    }

    response = client.get(app.url_path_for("get_issue", **path_params))

    assert response.status_code == 200, response.text
    assert response.json() == path_params
