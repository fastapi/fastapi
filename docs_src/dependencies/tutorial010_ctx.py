from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
