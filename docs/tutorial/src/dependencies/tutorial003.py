from typing import List

from pydantic import BaseModel

from fastapi import Cookie, Depends, FastAPI

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
async def read_interests(
    tracked_interests: InterestsTracker = Depends(get_tracked_interests)
):
    response = {"interests": tracked_interests.interests}
    return response
