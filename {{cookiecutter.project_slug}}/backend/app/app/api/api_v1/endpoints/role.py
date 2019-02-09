from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from app.core.jwt import get_current_user
from app.crud.user import check_if_user_is_active, check_if_user_is_superuser
from app.crud.utils import ensure_enums_to_strs
from app.models.role import RoleEnum, Roles
from app.models.user import UserInDB

router = APIRouter()


@router.get("/roles/", response_model=Roles)
def route_roles_get(current_user: UserInDB = Depends(get_current_user)):
    """
    Retrieve roles
    """
    if not check_if_user_is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not (check_if_user_is_superuser(current_user)):
        raise HTTPException(
            status_code=400, detail="The current user does not have enogh privileges"
        )
    roles = ensure_enums_to_strs(RoleEnum)
    return {"roles": roles}
