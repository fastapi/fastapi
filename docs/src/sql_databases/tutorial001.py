from fastapi import FastAPI
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

# SQLAlchemy specific code, as with any other app
SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

db_session = Session()

first_user = db_session.query(User).first()
if not first_user:
    u = User(email="johndoe@example.com", hashed_password="notreallyhashed")
    db_session.add(u)
    db_session.commit()

db_session.close()


# Utility
def get_user(db_session, user_id: int):
    return db_session.query(User).filter(User.id == user_id).first()


# FastAPI specific code
app = FastAPI()


@app.get("/users/{user_id}")
def read_user(request: Request, user_id: int):
    user = get_user(request.state.db, user_id=user_id)
    return user


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
