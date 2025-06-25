class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


@app.get("/")
async def get_root(db: Annotated[DBSession, Depends(MySuperContextManager)]): ...
