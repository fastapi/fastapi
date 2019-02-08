import pytest
import sqlalchemy

from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()

try:
    DATABASE_URL = "postgresql://foo:bar@localhost/fastapi"
except KeyError:  # pragma: no cover
    pytest.skip("DATABASE_URL is not set", allow_module_level=True)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


@app.get("/")
def read_root(request: Request):
    query = notes.select()
    results = await request.database.fetchall(query)
    return {"Hello": results}
