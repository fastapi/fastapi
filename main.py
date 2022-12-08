from fastapi import APIRouter, Depends, FastAPI, Request

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
