async def get_db():
    db = type("DBSession", (), {"close": lambda self: None})()
    try:
        yield db
    finally:
        db.close()
