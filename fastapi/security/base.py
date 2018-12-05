from enum import Enum
from pydantic import BaseModel, Schema

__all__ = ["Types", "SecurityBase"]


class Types(Enum):
    apiKey = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    openIdConnect = "openIdConnect"


class SecurityBase(BaseModel):
    scheme_name: str = None
    type_: Types = Schema(..., alias="type")
    description: str = None
