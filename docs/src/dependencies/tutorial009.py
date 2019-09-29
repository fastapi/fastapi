from sql_databases.sql_app.database import SessionLocal


class ContextSessionLocal:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with ContextSessionLocal() as db:
        yield db
