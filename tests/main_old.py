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

from .endpoints.a import router as router_a
from .endpoints.b import router as router_b

app = FastAPI()


app.include_router(router_a)
app.include_router(router_b, prefix="/b")


@app.get("/cookie")
def get_cookie(coo=Cookie(None)):
    return coo


@app.get("/header")
def get_header(head_name=Header(None)):
    return head_name


@app.get("/header_under")
def get_header(head_name=Header(None, convert_underscores=False)):
    return head_name


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


@app.put("/items/{item_id}")
def put_item(item_id: str, item: Item):
    return item


@app.post("/items/")
def post_item(item: Item):
    return item


@app.post("/items-all-params/{item_id}")
def post_items_all_params(
    item_id: str = Path(...),
    body: Item = Body(...),
    query_a: int = Query(None),
    query_b=Query(None),
    coo: str = Cookie(None),
    x_head: int = Header(None),
    x_under: str = Header(None, convert_underscores=False),
):
    return {
        "item_id": item_id,
        "body": body,
        "query_a": query_a,
        "query_b": query_b,
        "coo": coo,
        "x_head": x_head,
        "x_under": x_under,
    }


@app.post("/items-all-params-defaults/{item_id}")
def post_items_all_params_default(
    item_id: str,
    body_item_a: Item,
    body_item_b: Item,
    query_a: int,
    query_b: int,
    coo: str = Cookie(None),
    x_head: int = Header(None),
    x_under: str = Header(None, convert_underscores=False),
):
    return {
        "item_id": item_id,
        "body_item_a": body_item_a,
        "body_item_b": body_item_b,
        "query_a": query_a,
        "query_b": query_b,
        "coo": coo,
        "x_head": x_head,
        "x_under": x_under,
    }


@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    return item_id


@app.options("/options/")
def options():
    return JSONResponse(headers={"x-fastapi": "fast"})


@app.head("/head/")
def head():
    return {"not sent": "nope"}


@app.patch("/patch/{user_id}")
def patch(user_id: str, increment: float):
    return {"user_id": user_id, "total": 5 + increment}


@app.trace("/trace/")
def trace():
    return PlainTextResponse(media_type="message/http")


@app.get("/model", response_model=Item, status_code=HTTP_202_ACCEPTED)
def model():
    return {"name": "Foo", "price": "5.0", "password": "not sent"}


@app.get(
    "/metadata",
    tags=["tag1", "tag2"],
    summary="The summary",
    description="The description",
    response_description="Response description",
    deprecated=True,
    operation_id="a_very_long_and_strange_operation_id",
)
def get_meta():
    return "Foo"


@app.get("/html", content_type=HTMLResponse)
def get_html():
    return """
    <html>
    <body>
    <h1>
    Some text inside
    </h1>
    </body>
    </html>
    """


class FakeDB:
    def __init__(self):
        self.data = {
            "johndoe": {
                "username": "johndoe",
                "password": "shouldbehashed",
                "fist_name": "John",
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
    fist_name: str
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
    fist_name: str
    last_name: str


@app.get("/dependency", response_model=UserOut)
def get_dependency(user: UserInDB = Depends(require_user)):
    return user
