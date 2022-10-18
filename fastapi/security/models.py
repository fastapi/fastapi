# The file is presented as part of logical separation of
# security models that reside in a single place.

from fastapi.openapi.models import SecurityBase as SecurityBaseModel
from pydantic import BaseModel


class SecurityBase:
    model: SecurityBaseModel
    scheme_name: str


class APIKeyBase(SecurityBase):
    pass


class HTTPBasicCredentials(BaseModel):
    username: str
    password: str


class HTTPAuthorizationCredentials(BaseModel):
    scheme: str
    credentials: str
