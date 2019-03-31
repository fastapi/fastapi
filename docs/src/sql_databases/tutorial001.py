from fastapi import Depends, FastAPI
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from starlette.responses import Response

# SQLAlchemy specific code, as with any other app
SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomBase:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)


Base.metadata.create_all(bind=engine)

db_session = SessionLocal()

first_user = db_session.query(User).first()
if not first_user:
    u = User(email="johndoe@example.com", hashed_password="notreallyhashed")
    db_session.add(u)
    db_session.commit()

db_session.close()


# Utility
def get_user(db_session: Session, user_id: int):
    return db_session.query(User).filter(User.id == user_id).first()


# Dependency
def get_db(request: Request):
    return request.state.db


# FastAPI specific code
app = FastAPI()


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    return user


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response('', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
