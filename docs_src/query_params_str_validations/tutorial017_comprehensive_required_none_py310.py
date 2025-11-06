from typing import Annotated, Union

from fastapi import FastAPI, Query, HTTPException

app = FastAPI()


@app.get("/items/basic/")
async def read_items_basic(
    q: Annotated[Union[str, None], Query(min_length=3)]
):
    """
    Basic example: Required query parameter that can be None.
    
    Usage examples:
    - GET /items/basic/?q=test -> filters by "test"
    - GET /items/basic/?q=null -> returns all items (q treated as None)
    - GET /items/basic/ -> 422 error (parameter required)
    - GET /items/basic/?q=ab -> 422 error (too short)
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    
    # Handle explicit None case
    if q == "null":
        q = None
    
    if q is not None:
        results.update({"q": q, "filtered": True})
    else:
        results.update({"q": None, "filtered": False})
    
    return results


@app.get("/items/advanced/")
async def read_items_advanced(
    q: Annotated[Union[str, None], Query(min_length=3)],
    include_metadata: Annotated[bool, Query()] = False
):
    """
    Advanced example: Multiple required parameters with None handling.
    
    This shows how to handle multiple query parameters where some
    can be None and others have different types.
    
    Usage examples:
    - GET /items/advanced/?q=search&include_metadata=true
    - GET /items/advanced/?q=null&include_metadata=false  
    - GET /items/advanced/?q=search (include_metadata defaults to false)
    """
    # Convert "null" string to actual None
    if q == "null":
        q = None
    
    # Simulate database items
    all_items = [
        {"item_id": "Foo", "tags": ["tag1", "tag2"], "active": True},
        {"item_id": "Bar", "tags": ["tag3"], "active": False},
        {"item_id": "Baz", "tags": ["tag1"], "active": True}
    ]
    
    # Filter items if query is provided
    if q is not None:
        filtered_items = [
            item for item in all_items 
            if q.lower() in item["item_id"].lower() or 
               any(q.lower() in tag.lower() for tag in item["tags"])
        ]
    else:
        filtered_items = all_items
    
    # Remove metadata if not requested
    if not include_metadata:
        filtered_items = [
            {"item_id": item["item_id"]} 
            for item in filtered_items
        ]
    
    return {
        "items": filtered_items,
        "query_used": q,
        "total_found": len(filtered_items),
        "metadata_included": include_metadata
    }


@app.get("/items/validation/")
async def read_items_with_custom_validation(
    q: Annotated[Union[str, None], Query(min_length=3)]
):
    """
    Example with custom validation and error handling.
    
    This shows how to add custom business logic validation
    while still using FastAPI's automatic validation.
    """
    # Handle explicit None case
    if q == "null":
        q = None
    
    # Custom validation (after FastAPI's automatic validation)
    if q is not None:
        # Example: Reject certain reserved words
        reserved_words = ["admin", "system", "root"]
        if q.lower() in reserved_words:
            raise HTTPException(
                status_code=400,
                detail=f"Query '{q}' is a reserved word and cannot be used for searching"
            )
        
        # Example: Convert to proper search format
        q = q.strip().lower()
    
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    
    if q is not None:
        results.update({
            "q": q,
            "search_performed": True,
            "note": "Query has been normalized to lowercase"
        })
    else:
        results.update({
            "q": None,
            "search_performed": False,
            "note": "No search query provided (null value received)"
        })
    
    return results