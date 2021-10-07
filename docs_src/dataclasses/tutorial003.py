from dataclasses import field  # (1)
from typing import List, Optional

from fastapi import FastAPI
from pydantic.dataclasses import dataclass  # (2)


@dataclass
class Item:
    name: str
    description: Optional[str] = None


@dataclass
class Author:
    name: str
    items: List[Item] = field(default_factory=list)  # (3)


app = FastAPI()


@app.post("/authors/{author_id}/items/", response_model=Author)  # (4)
async def create_author_items(author_id: str, items: List[Item]):  # (5)
    return {"name": author_id, "items": items}  # (6)


@app.get("/authors/", response_model=List[Author])  # (7)
def get_authors():  # (8)
    return [  # (9)
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]
