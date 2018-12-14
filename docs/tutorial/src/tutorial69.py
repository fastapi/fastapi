from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.models.config import USERPROFILE_DOC_TYPE
from couchbase import LOCKMODE_WAIT
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster, PasswordAuthenticator


def get_bucket():
    cluster = Cluster("couchbase://couchbasehost:8091")
    authenticator = PasswordAuthenticator("username", "password")
    cluster.authenticate(authenticator)
    bucket: Bucket = cluster.open_bucket("bucket_name", lockmode=LOCKMODE_WAIT)
    return bucket


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str

    class Meta:
        key: Optional[str] = None


def get_user_doc_id(username):
    return f"userprofile::{username}"


def get_user(bucket: Bucket, username: str):
    doc_id = get_user_doc_id(username)
    result = bucket.get(doc_id, quiet=True)
    if not result.value:
        return None
    user = UserInDB(**result.value)
    user.Meta.key = result.key
    return user


# FastAPI specific code
app = FastAPI()


@app.get("/users/{username}")
def read_user(username: str):
    bucket = get_bucket()
    user = get_user(bucket=bucket, username=username)
    return user
