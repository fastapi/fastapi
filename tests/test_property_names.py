"""
Tests for PropertyNames constraint support in FastAPI.
"""

from typing import Dict

from fastapi import FastAPI
from fastapi.schema import PropertyNames
from pydantic import BaseModel
from typing_extensions import Annotated


def test_property_names_creation():
    """Test PropertyNames object creation and validation."""
    # Test pattern constraint
    pn1 = PropertyNames(pattern="^test_")
    assert pn1.get_constraint_schema() == {"pattern": "^test_"}

    # Test multiple constraints
    pn2 = PropertyNames(min_length=5, max_length=20, pattern="^[a-z]+$")
    expected = {"minLength": 5, "maxLength": 20, "pattern": "^[a-z]+$"}
    assert pn2.get_constraint_schema() == expected

    # Test schema constraint
    pn3 = PropertyNames(schema={"type": "string", "format": "email"})
    expected = {"type": "string", "format": "email"}
    assert pn3.get_constraint_schema() == expected

    # Test empty constraint should raise error
    try:
        PropertyNames()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert (
            "PropertyNames constraint must specify at least one validation rule"
            in str(e)
        )


def test_property_names_pattern_constraint():
    """Test PropertyNames with pattern constraint in FastAPI schema generation."""

    class ModelWithPropertyNames(BaseModel):
        properties: Annotated[Dict[str, str], PropertyNames(pattern="^prefix_")]

    app = FastAPI()

    @app.post("/test")
    def test_endpoint(data: ModelWithPropertyNames):
        return data

    # Get the OpenAPI schema
    openapi_schema = app.openapi()

    # Find the schema for our model
    model_schema = None
    for schema_name, schema_def in openapi_schema["components"]["schemas"].items():
        if schema_name == "ModelWithPropertyNames":
            properties_field = schema_def["properties"]["properties"]
            if "propertyNames" in properties_field:
                model_schema = properties_field
                break

    assert model_schema is not None, "Could not find model schema with propertyNames"

    # Verify the propertyNames constraint is present
    property_names_constraint = model_schema["propertyNames"]
    assert property_names_constraint["pattern"] == "^prefix_"

    # Verify the full schema structure
    expected_keys = {"type", "additionalProperties", "propertyNames", "title"}
    assert set(model_schema.keys()) >= expected_keys


def test_property_names_complex_constraints():
    """Test PropertyNames with multiple constraints."""

    class ComplexPropertyNames(BaseModel):
        config_vars: Annotated[
            Dict[str, str],
            PropertyNames(min_length=3, max_length=50, pattern="^[A-Z_]+$"),
        ]

    app = FastAPI()

    @app.post("/test")
    def test_endpoint(data: ComplexPropertyNames):
        return data

    # Get the OpenAPI schema
    openapi_schema = app.openapi()

    # Find the schema for our model
    model_schema = None
    for schema_name, schema_def in openapi_schema["components"]["schemas"].items():
        if schema_name == "ComplexPropertyNames":
            config_vars_field = schema_def["properties"]["config_vars"]
            if "propertyNames" in config_vars_field:
                model_schema = config_vars_field
                break

    assert model_schema is not None, "Could not find model schema with propertyNames"

    # Verify the propertyNames constraint has all expected properties
    property_names_constraint = model_schema["propertyNames"]
    assert property_names_constraint["pattern"] == "^[A-Z_]+$"
    assert property_names_constraint["minLength"] == 3
    assert property_names_constraint["maxLength"] == 50


def test_property_names_schema_constraint():
    """Test PropertyNames with custom schema constraint."""

    class SchemaPropertyNames(BaseModel):
        allowed_keys: Annotated[
            Dict[str, int],
            PropertyNames(schema={"type": "string", "enum": ["key1", "key2", "key3"]}),
        ]

    app = FastAPI()

    @app.post("/test")
    def test_endpoint(data: SchemaPropertyNames):
        return data

    # Get the OpenAPI schema
    openapi_schema = app.openapi()

    # Find the schema for our model
    model_schema = None
    for schema_name, schema_def in openapi_schema["components"]["schemas"].items():
        if schema_name == "SchemaPropertyNames":
            allowed_keys_field = schema_def["properties"]["allowed_keys"]
            if "propertyNames" in allowed_keys_field:
                model_schema = allowed_keys_field
                break

    assert model_schema is not None, "Could not find model schema with propertyNames"

    # Verify the propertyNames constraint with custom schema
    property_names_constraint = model_schema["propertyNames"]
    assert property_names_constraint["type"] == "string"
    assert property_names_constraint["enum"] == ["key1", "key2", "key3"]


def test_property_names_no_constraint():
    """Test that models without PropertyNames constraints work normally."""

    class NormalModel(BaseModel):
        properties: Dict[str, str]

    app = FastAPI()

    @app.post("/test")
    def test_endpoint(data: NormalModel):
        return data

    # Get the OpenAPI schema
    openapi_schema = app.openapi()

    # Find the schema for our model
    for schema_name, schema_def in openapi_schema["components"]["schemas"].items():
        if schema_name == "NormalModel":
            properties_field = schema_def["properties"]["properties"]
            # Should not have propertyNames constraint
            assert "propertyNames" not in properties_field
            break
    else:
        assert False, "Could not find NormalModel schema"


def test_property_names_kwargs():
    """Test PropertyNames with additional kwargs."""
    pn = PropertyNames(format="email", description="Email addresses")
    constraint_schema = pn.get_constraint_schema()

    assert constraint_schema["format"] == "email"
    assert constraint_schema["description"] == "Email addresses"


def test_property_names_repr():
    """Test PropertyNames string representation."""
    pn = PropertyNames(pattern="^test_")
    repr_str = repr(pn)

    assert "PropertyNames" in repr_str
    assert "pattern" in repr_str
    assert "^test_" in repr_str
