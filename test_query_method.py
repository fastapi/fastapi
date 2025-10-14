#!/usr/bin/env python3
"""
Test script for the new QUERY method in FastAPI
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

class SearchQuery(BaseModel):
    terms: List[str]
    filters: Dict[str, Any] = {}
    limit: int = 10

@app.query("/search/")
def search_items(query: SearchQuery):
    """
    Search for items using the QUERY method.
    
    This demonstrates the new QUERY HTTP method that allows
    complex request bodies for search operations.
    """
    return {
        "results": [
            {"id": 1, "name": "Item 1", "matches": query.terms},
            {"id": 2, "name": "Item 2", "matches": query.terms}
        ],
        "query": query.dict(),
        "total": 2
    }

@app.get("/")
def read_root():
    return {"message": "FastAPI with QUERY method support"}

if __name__ == "__main__":
    import uvicorn
    print("Testing FastAPI QUERY method implementation...")
    print("Visit http://localhost:8000/docs to see the QUERY endpoint in action!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
