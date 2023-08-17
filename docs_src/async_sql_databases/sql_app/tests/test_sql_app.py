from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# connect_args is ONLY for sqlite, remove if using PostgreSQL or other.
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


@app.on_event("startup")
async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def override_get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_user():
    with TestClient(app) as client:
        response = client.post(
            "/users/",
            json={"email": "deadpool@example.com", "password": "chimichangas4life"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "deadpool@example.com"
        assert "id" in data
        user_id = data["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "deadpool@example.com"
        assert data["id"] == user_id
