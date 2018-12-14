from fastapi import APIRouter

router = APIRouter()


@router.get("/users/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}


@router.get("/users/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}
