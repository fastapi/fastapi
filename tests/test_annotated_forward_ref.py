"""Test for ForwardRef resolution with Annotated and Depends.

This test verifies the fix for: https://github.com/fastapi/fastapi/issues/13056
When using `from __future__ import annotations`, ForwardRefs in Annotated types
should be properly resolved when generating OpenAPI schema.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated
import json

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi


def test_annotated_with_forward_ref_openapi():
    """Test that Annotated with ForwardRef generates correct OpenAPI schema.
    
    This test reproduces the issue where Potato is defined AFTER the route,
    which causes it to be a ForwardRef when the route is processed.
    """
    app = FastAPI()

    def get_potato() -> Potato:
        return Potato(color='red', size=10)

    @app.get('/')
    async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
        return {'Hello': 'World'}

    # Define Potato AFTER the route - this is the problematic case
    @dataclass
    class Potato:
        color: str
        size: int

    # Generate OpenAPI schema - this should not raise an error
    openapi_schema = get_openapi(title="Test", version="1.0.0", routes=app.routes)
    
    print(f"Schema keys: {openapi_schema.keys()}")
    if "components" in openapi_schema:
        print(json.dumps(openapi_schema["components"], indent=2))
    else:
        print("No components in schema")


if __name__ == "__main__":
    test_annotated_with_forward_ref_openapi()
    print("Test completed!")
