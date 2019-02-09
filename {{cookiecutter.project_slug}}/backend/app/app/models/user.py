from typing import List, Optional, Union

from pydantic import BaseModel

from app.models.config import USERPROFILE_DOC_TYPE
from app.models.role import RoleEnum


# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None
    admin_roles: Optional[List[Union[str, RoleEnum]]] = None
    admin_channels: Optional[List[Union[str, RoleEnum]]] = None
    disabled: Optional[bool] = None


class UserBaseInDB(UserBase):
    username: str
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserInCreate(UserBaseInDB):
    password: str
    admin_roles: List[Union[str, RoleEnum]] = []
    admin_channels: List[Union[str, RoleEnum]] = []
    disabled: bool = False


# Properties to receive via API on update
class UserInUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserBaseInDB):
    pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str


class UserSyncIn(UserBase):
    name: str
    password: Optional[str] = None
