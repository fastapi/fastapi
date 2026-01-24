from datetime import datetime
from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: Union[datetime, None] = None
    friends: list[int] = []  # List of Integer


external_data = {
    "id": "123",
    "signup_ts": "2026-01-01 22:22",
    "friends": [1, 2, 3],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2026, 1, 1, 22, 22) friends=[1, 2, 3]
print(user.id)
# > 123
