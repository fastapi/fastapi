# Required Parameters That Can Be None - FastAPI Documentation Enhancement

## Overview

This enhancement addresses a common question about FastAPI query parameters: **How to create a parameter that is required (must be provided by the client) but can explicitly be set to None?**

## The Problem

Users often want to create APIs where:
1. A parameter **must be provided** by the client (not optional)
2. The parameter **can be explicitly set to None** to indicate "no filtering" or similar behavior
3. Validation rules still apply when the parameter is not None

The existing documentation shows either:
- Optional parameters: `param: str | None = None` 
- Required parameters: `param: str`

But doesn't clearly demonstrate the middle ground: **required but nullable**.

## The Solution

### Basic Approach

```python
from typing import Annotated, Union
from fastapi import FastAPI, Query

@app.get("/items/")
async def read_items(
    q: Annotated[Union[str, None], Query(min_length=3)]
):
    # Handle explicit None case
    if q == "null":
        q = None
    
    if q is not None:
        # Filter logic here
        return {"items": [...], "filtered_by": q}
    else:
        # Return all items
        return {"items": [...], "filtered": False}
```

### Key Points

1. **No default value** - Makes the parameter required
2. **Union[str, None]** - Allows both string and None values  
3. **Handle "null" string** - Convert string "null" to Python None
4. **Validation applies** - min_length=3 still enforced for non-None values

### Usage Examples

```bash
# ✅ Valid - searches for "python" 
GET /items/?q=python

# ✅ Valid - explicitly no filtering (null converted to None)
GET /items/?q=null

# ❌ Invalid - parameter required
GET /items/

# ❌ Invalid - too short (validation applies)
GET /items/?q=ab
```

## Implementation Files

### Basic Example
- `tutorial016_required_can_be_none_py310.py` - Simple demonstration
- `tutorial016_required_can_be_none_an.py` - Compatible with older Python versions

### Comprehensive Example  
- `tutorial017_comprehensive_required_none_py310.py` - Advanced patterns including:
  - Multiple required parameters with different types
  - Custom validation and error handling
  - Real-world filtering logic
  - Proper error messages

## Why This Enhancement Matters

1. **Addresses Real User Need** - Issue #12419 shows this is a genuine pain point
2. **Fills Documentation Gap** - Current docs don't cover this specific pattern  
3. **Provides Working Code** - Complete, tested examples ready to use
4. **Shows Best Practices** - Error handling, validation, and API design patterns

## Testing

All examples include comprehensive test coverage showing:
- ✅ Valid string parameters with filtering
- ✅ Explicit null handling ("null" → None)
- ❌ Missing parameter validation (422 error)
- ❌ Validation rule enforcement (min_length, etc.)

## Related Documentation

This enhancement connects to existing FastAPI documentation:
- Query Parameters tutorial
- Parameter validation
- Request validation and error handling  
- Type hints and annotations

The examples follow FastAPI's established patterns while addressing the specific "required but nullable" use case.

## Community Impact

Expected to help:
- New FastAPI users encountering this common pattern
- Developers migrating from other frameworks with different parameter semantics
- API designers needing explicit null/empty state handling

This addresses a frequently asked question and provides clear, working solutions with comprehensive examples.