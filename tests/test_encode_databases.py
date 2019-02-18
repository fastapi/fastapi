import logging
from typing import List

import databases
import pytest
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from starlette.testclient import TestClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# docker run --name fastapi-postgres -e POSTGRES_PASSWORD=bar -e POSTGRES_USER=foo -e POSTGRES_DB=fastapi -p 5432:5432 -d postgres
try:
    DATABASE_URL = "postgresql://foo:bar@localhost/fastapi"
except KeyError:  # pragma: no cover
    pytest.skip("DATABASE_URL is not set", allow_module_level=True)

app = FastAPI()
database = databases.Database(DATABASE_URL, force_rollback=True)


@pytest.fixture(autouse=True, scope="function")
def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    engine.execute("DROP TABLE users")


metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("admin", sqlalchemy.Boolean, default=False),
)


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/users", response_model=List[UserIn])
async def list_users():
    query = users.select()
    results = await database.fetch_all(query)
    return results
    # return [r._row for r in results]


@app.post("/users", status_code=201)
async def add_user(user: UserIn):
    query = users.insert().values(**user.dict())
    result = await database.execute(query)
    return result


def test_databases_list():
    with TestClient(app) as client:
        for i in range(4):
            user = {
                "username": f"user{i}",
                "email": f"test{i}@test.com",
                "password": "1234",
            }
            response = client.post("/users", json=user)
            assert response.status_code == 201

        response = client.get("/users")
        assert response.status_code == 200
