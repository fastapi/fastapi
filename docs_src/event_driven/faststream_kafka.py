from pydantic import BaseModel
from fastapi import FastAPI
from faststream.kafka.fastapi import KafkaRouter


event_router = KafkaRouter()


class User(BaseModel):
    name: str
    age: int


@event_router.subscriber("user-created-topic")
async def user_created(user: User):
    print(f"User created by event: {user.name}, {user.age}")


app = FastAPI()
app.include_router(event_router)
