from typing import List, Set

from fastapi import Body, FastAPI, Path, Query, Depends, Cookie
from pydantic import BaseModel
from pydantic.types import UrlStr
from starlette.status import HTTP_201_CREATED
from starlette.responses import HTMLResponse

app = FastAPI()


class InterestsTracker(BaseModel):
    track_code: str
    interests: List[str]


fake_tracked_users_db = {
    "Foo": {"track_code": "Foo", "interests": ["sports", "movies"]},
    "Bar": {"track_code": "Bar", "interests": ["food", "shows"]},
    "Baz": {"track_code": "Baz", "interests": ["gaming", "virtual reality"]},
}


async def get_tracked_interests(track_code: str = Cookie(None)):
    if track_code in fake_tracked_users_db:
        track_dict = fake_tracked_users_db[track_code]
        track = InterestsTracker(**track_dict)
        return track
    return None


@app.get("/interests/")
async def read_interests(tracked_interests: InterestsTracker = Depends(get_tracked_interests)):
    response = {"interests": tracked_interests.interests}
    return response
