"""
FastAPI schema utilities including PropertyNames constraint support.
"""

from typing import Any, Dict, Optional

from pydantic.fields import FieldInfo


class PropertyNames:
    """
    A constraint class for specifying propertyNames validation in JSON Schema.

    This allows developers to specify patterns or schemas that all property names
    in a dictionary/object must match.

    Examples:
        # Pattern-based constraint
        PropertyNames(pattern="^prefix_")

        # Schema-based constraint
        PropertyNames(min_length=3, max_length=50)

        # Complex schema constraint
        PropertyNames(schema={"type": "string", "enum": ["key1", "key2", "key3"]})
    """

    def __init__(
        self,
        pattern: Optional[str] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        schema: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        """
        Initialize PropertyNames constraint.

        Args:
            pattern: Regular expression pattern that property names must match
            min_length: Minimum length for property names
            max_length: Maximum length for property names
            schema: Custom JSON schema for property names validation
            **kwargs: Additional JSON schema properties
        """
        self.constraint_schema: Dict[str, Any] = {}

        if pattern is not None:
            self.constraint_schema["pattern"] = pattern

        if min_length is not None:
            self.constraint_schema["minLength"] = min_length

        if max_length is not None:
            self.constraint_schema["maxLength"] = max_length

        if schema is not None:
            self.constraint_schema.update(schema)

        # Add any additional properties
        for key, value in kwargs.items():
            if value is not None:
                self.constraint_schema[key] = value

        if not self.constraint_schema:
            raise ValueError(
                "PropertyNames constraint must specify at least one validation rule"
            )

    def get_constraint_schema(self) -> Dict[str, Any]:
        """Get the JSON schema representation of this constraint."""
        return self.constraint_schema.copy()

    def __repr__(self) -> str:
        return f"PropertyNames({self.constraint_schema})"


def get_property_names_constraint(field_info: FieldInfo) -> Optional[Dict[str, Any]]:
    """
    Extract PropertyNames constraint from field metadata.

    Args:
        field_info: Pydantic FieldInfo object

    Returns:
        PropertyNames constraint schema or None if not found
    """
    if not hasattr(field_info, "metadata") or not field_info.metadata:
        return None

    for metadata_item in field_info.metadata:
        if isinstance(metadata_item, PropertyNames):
            return metadata_item.get_constraint_schema()

    return None


def apply_property_names_to_schema(
    schema: Dict[str, Any], property_names_constraint: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply PropertyNames constraint to a JSON schema.

    Args:
        schema: The JSON schema to modify
        property_names_constraint: The propertyNames constraint to apply

    Returns:
        Modified schema with propertyNames constraint
    """
    if schema.get("type") == "object":
        schema["propertyNames"] = property_names_constraint
    return schema
