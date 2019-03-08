from fastapi import (
    Body,
    Cookie,
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    Path,
    Query,
    Security,
)
from fastapi.security import (
    HTTPBasic,
    OAuth2,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from pydantic import BaseModel
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse
from starlette.status import HTTP_202_ACCEPTED

app = FastAPI()


@app.get("/security")
def get_security(sec=Security(HTTPBasic())):
    return sec


reusable_oauth2 = OAuth2(
    flows={
        "password": {
            "tokenUrl": "/token",
            "scopes": {"read:user": "Read a User", "write:user": "Create a user"},
        }
    }
)


@app.get("/security/oauth2")
def get_security_oauth2(sec=Security(reusable_oauth2, scopes=["read:user"])):
    return sec


@app.post("/token")
def post_token(request_data: OAuth2PasswordRequestForm = Form(...)):
    data = request_data.parse()
    access_token = data.username + ":" + data.password
    return {"access_token": access_token}


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool


class FakeDB:
    def __init__(self):
        self.data = {
            "johndoe": {
                "username": "johndoe",
                "password": "shouldbehashed",
                "first_name": "John",
                "last_name": "Doe",
            }
        }


class DBConnectionManager:
    def __init__(self):
        self.db = FakeDB()

    def __call__(self):
        return self.db


connection_manager = DBConnectionManager()


class TokenUserData(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


def require_token(
    token: str = Security(reusable_oauth2, scopes=["read:user", "write:user"])
):
    raw_token = token.replace("Bearer ", "")
    # Never do this plaintext password usage in production
    username, password = raw_token.split(":")
    return TokenUserData(username=username, password=password)


def require_user(
    db: FakeDB = Depends(connection_manager),
    user_data: TokenUserData = Depends(require_token),
):
    return db.data[user_data.username]


class UserOut(BaseModel):
    username: str
    first_name: str
    last_name: str


@app.get("/dependency", response_model=UserOut)
def get_dependency(user: UserInDB = Depends(require_user)):
    return user
