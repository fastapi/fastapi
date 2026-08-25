class MySuperContextManager:
    def __init__(self):
        self.db = type("DBSession", (), {"close": lambda self: None})()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
