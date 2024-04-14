# Async MongoDB with Motor

**FastAPI** can also be integrated with any <abbr title="Distributed database (Big Data), also 'Not Only SQL'">NoSQL</abbr>.

This includes, but is not limited to:

* **Cassandra**
* **CouchDB**
* **ArangoDB**
* **ElasticSearch**
* etc

[Motor](https://motor.readthedocs.io/en/stable/index.html) is an asynchronous Python driver for MongoDB.

## Install Motor

```bash
pip install motor
```

## Create a MongoDB Client

```Python hl_lines="10"
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None

db = Database()

@app.on_event("startup")
async def startup_db_client():
    db.client = AsyncIOMotorClient("mongodb://localhost:27017")

@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()
```

## Interact with MongoDB

```Python hl_lines="7-8"
from fastapi import FastAPI

app = FastAPI()

@app.post("/items/")
async def create_item(item: dict) -> str:
    collection = db.client.mydatabase.items
    result = await collection.insert_one(item)
    return {"id": str(result.inserted_id)}
```

## Integrate Beanie ODM

[Beanie](https://roman-right.github.io/beanie/) is an async Python object-document mapper (ODM) built on top of Motor and Pydantic.
You can extend the Motor example above by defining `Document` models and adding an initialization call to DB startup.

```Python
from beanie import Document

class Item(Document):
    name: str
    description: str
    tax: float
```

Initialize Beanie with Motor client:

```Python hl_lines="8-11"
from beanie import init_beanie

# ...

@app.on_event("startup")
async def startup_db_client():
    db.client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=db.client.mydatabase,  # Use your database name
        document_models=[Item]
    )
```

## Use Beanie Mapped Object

Since `Item` is also a Pydantic model, it can be integrated into FastAPI's [response model](https://fastapi.tiangolo.com/tutorial/response-model/).

```Python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude={"tax"}
)
async def get_item(item_id: str) -> Item:
    item = await Item.find_one({"_id": item_id})
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail="Item not found")
```
