#!/usr/bin/env python3

"""
Example: Basic QUERY method usage in FastAPI.

This example demonstrates how to use the QUERY HTTP method for simple queries.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class SimpleQuery(BaseModel):
    search_term: str
    limit: Optional[int] = 10


@app.query("/search")
def search_items(query: SimpleQuery):
    """
    Search for items using the QUERY method.
    
    The QUERY method allows sending complex search parameters in the request body
    instead of URL parameters, making it ideal for complex queries.
    """
    # Simulate search logic
    results = [
        f"Item {i}: {query.search_term}" 
        for i in range(1, min(query.limit + 1, 6))
    ]
    
    return {
        "query": query.search_term,
        "limit": query.limit,
        "results": results,
        "total_found": len(results)
    }
