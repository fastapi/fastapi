from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from sql_databases.sql_app.database import SessionLocal

app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get-db-check")
async def db_session_dependency_check(db: Session = Depends(get_db)):
    return isinstance(db, Session)
