from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", summary="Get all Items")
async def get_items():
    """
    Get all items with all the information:

    ```mermaid
    sequenceDiagram
        App->>API: GET /items/
        API->>DB: SELECT * FROM items
        DB-->>API: #
        API-->>App: #
    ```
    """
    return []
