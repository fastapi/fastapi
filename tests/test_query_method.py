"""
Tests for the QUERY HTTP method implementation in FastAPI
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel


class SearchQuery(BaseModel):
    terms: List[str]
    filters: Dict[str, Any] = {}
    limit: int = 10


def test_query_method_exists_on_fastapi():
    """Test that QUERY method exists on FastAPI class"""
    app = FastAPI()
    assert hasattr(app, "query")
    assert callable(app.query)


def test_query_method_exists_on_router():
    """Test that QUERY method exists on APIRouter class"""
    router = APIRouter()
    assert hasattr(router, "query")
    assert callable(router.query)


def test_query_method_decorator_works():
    """Test that QUERY method decorator can be applied"""
    app = FastAPI()

    @app.query("/search")
    def search_items(query: SearchQuery):
        return {"results": f"Searching for {query.terms}"}

    # Test that the decorator worked and route was added
    routes = [route for route in app.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0


def test_query_method_with_router_decorator():
    """Test that QUERY method decorator works with APIRouter"""
    router = APIRouter()

    @router.query("/items")
    def query_items(query: SearchQuery):
        return {"items": query.terms, "filters": query.filters}

    # Test that the decorator worked and route was added
    routes = [route for route in router.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0


def test_query_method_with_dependencies():
    """Test QUERY method with dependencies"""
    app = FastAPI()

    def get_current_user():
        return {"user_id": 123}

    @app.query("/protected", dependencies=[Depends(get_current_user)])
    def protected_query(query: SearchQuery):
        return {"protected": True, "query": query.dict()}

    # Test that the decorator worked
    routes = [route for route in app.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0


def test_query_method_with_all_parameters():
    """Test QUERY method with comprehensive parameters"""
    app = FastAPI()

    @app.query(
        "/advanced",
        response_model=dict,
        status_code=200,
        tags=["search"],
        summary="Advanced search",
        description="Perform advanced search operations",
        response_description="Search results",
        deprecated=False,
        operation_id="advanced_search",
        responses={404: {"description": "Not found"}},
        name="advanced_search_endpoint",
        include_in_schema=True,
        generate_unique_id_function=lambda route: f"query_{route.name}",
    )
    def advanced_search(query: SearchQuery):
        return {"advanced": True, "query": query.dict()}

    # Verify route was created
    routes = [route for route in app.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0


def test_router_query_method_with_all_parameters():
    """Test APIRouter QUERY method with comprehensive parameters"""
    router = APIRouter()

    @router.query(
        "/router-advanced",
        response_model=dict,
        status_code=201,
        tags=["router-search"],
        summary="Router advanced search",
        description="Perform advanced search via router",
        response_description="Router search results",
        deprecated=False,
        operation_id="router_advanced_search",
        responses={400: {"description": "Bad request"}},
        name="router_advanced_search_endpoint",
        include_in_schema=True,
        generate_unique_id_function=lambda route: f"router_query_{route.name}",
    )
    def router_advanced_search(query: SearchQuery):
        return {"router_advanced": True, "query": query.dict()}

    # Verify route was created
    routes = [route for route in router.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0


def test_query_method_with_callbacks():
    """Test QUERY method with callbacks parameter"""
    app = FastAPI()

    @app.query("/with-callbacks", callbacks=None)
    def query_with_callbacks(query: SearchQuery):
        return {"callbacks": "tested", "query": query.dict()}

    # Verify route was created
    routes = [route for route in app.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0


def test_query_method_with_openapi_extra():
    """Test QUERY method with openapi_extra parameter"""
    app = FastAPI()

    @app.query("/with-openapi-extra", openapi_extra={"x-custom": "value"})
    def query_with_openapi_extra(query: SearchQuery):
        return {"openapi_extra": "tested", "query": query.dict()}

    # Verify route was created
    routes = [route for route in app.routes if hasattr(route, "methods")]
    query_routes = [
        route for route in routes if "QUERY" in getattr(route, "methods", [])
    ]
    assert len(query_routes) > 0
