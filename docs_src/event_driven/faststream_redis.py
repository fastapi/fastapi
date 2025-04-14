from fastapi import FastAPI
from faststream.redis.fastapi import RedisRouter
from pydantic import BaseModel

event_router = RedisRouter()


class User(BaseModel):
    name: str
    age: int


@event_router.subscriber("user.created")
async def user_created(user: User):
    print(f"User created by event: {user.name}, {user.age}")


app = FastAPI()
app.include_router(event_router)
