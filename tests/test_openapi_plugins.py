"""
Tests for the OpenAPI plugin system.
"""

from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.openapi.plugins import (
    OpenAPIPluginBase,
    OpenAPIPluginSettings,
    PluginExecutor,
    PluginRegistry,
    create_plugin,
)
from fastapi.testclient import TestClient
from pydantic import BaseModel


# =============================================================================
# Test Models
# =============================================================================


class Item(BaseModel):
    name: str
    price: float


# =============================================================================
# Test Plugins
# =============================================================================


class CustomExtensionPlugin(OpenAPIPluginBase):
    """Plugin that adds custom x- extensions to all operations."""

    @property
    def name(self) -> str:
        return "custom-extension"

    @property
    def priority(self) -> int:
        return 50  # Higher priority (runs first)

    def modify_operation(
        self,
        route: Any,
        method: str,
        operation: dict[str, Any],
    ) -> dict[str, Any]:
        operation["x-custom-extension"] = True
        operation["x-route-name"] = route.name
        return operation


class SchemaModifierPlugin(OpenAPIPluginBase):
    """Plugin that modifies the schema after generation."""

    @property
    def name(self) -> str:
        return "schema-modifier"

    def modify_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        schema["x-generated-by"] = "FastAPI Plugin System"
        if "info" in schema:
            schema["info"]["x-plugin-version"] = "1.0"
        return schema


class PostGenerationPlugin(OpenAPIPluginBase):
    """Plugin that runs after schema generation."""

    @property
    def name(self) -> str:
        return "post-generation"

    @property
    def priority(self) -> int:
        return 200  # Lower priority (runs last)

    def post_schema_generation(self, schema: dict[str, Any]) -> dict[str, Any]:
        schema["x-post-processed"] = True
        return schema


class PreSchemaPlugin(OpenAPIPluginBase):
    """Plugin that tracks pre_schema_generation calls."""

    def __init__(self):
        self.pre_called = False
        self.settings_received: OpenAPIPluginSettings | None = None

    @property
    def name(self) -> str:
        return "pre-schema"

    def pre_schema_generation(
        self,
        app: FastAPI,
        settings: OpenAPIPluginSettings,
    ) -> None:
        self.pre_called = True
        self.settings_received = settings


class ErrorPlugin(OpenAPIPluginBase):
    """Plugin that raises errors for testing error handling."""

    @property
    def name(self) -> str:
        return "error-plugin"

    def modify_operation(
        self,
        route: Any,
        method: str,
        operation: dict[str, Any],
    ) -> dict[str, Any]:
        raise ValueError("Intentional error for testing")


# =============================================================================
# Plugin Registry Tests
# =============================================================================


class TestPluginRegistry:
    """Tests for PluginRegistry class."""

    def test_register_plugin(self):
        """Test basic plugin registration."""
        registry = PluginRegistry()
        plugin = CustomExtensionPlugin()
        registry.register(plugin)

        assert "custom-extension" in registry
        assert len(registry) == 1
        assert registry.get_plugin("custom-extension") is plugin

    def test_register_duplicate_raises(self):
        """Test that registering duplicate name raises error."""
        registry = PluginRegistry()
        plugin1 = CustomExtensionPlugin()
        plugin2 = CustomExtensionPlugin()

        registry.register(plugin1)
        with pytest.raises(ValueError, match="already registered"):
            registry.register(plugin2)

    def test_register_with_replace(self):
        """Test replacing an existing plugin."""
        registry = PluginRegistry()
        plugin1 = CustomExtensionPlugin()
        plugin2 = CustomExtensionPlugin()

        registry.register(plugin1)
        registry.register(plugin2, replace=True)

        assert registry.get_plugin("custom-extension") is plugin2

    def test_unregister_plugin(self):
        """Test unregistering a plugin."""
        registry = PluginRegistry()
        plugin = CustomExtensionPlugin()
        registry.register(plugin)

        assert registry.unregister("custom-extension") is True
        assert "custom-extension" not in registry
        assert registry.unregister("custom-extension") is False

    def test_enable_disable_plugin(self):
        """Test enabling and disabling plugins."""
        registry = PluginRegistry()
        plugin = CustomExtensionPlugin()
        registry.register(plugin, enabled=False)

        assert not registry.is_enabled("custom-extension")
        assert len(registry.get_active_plugins()) == 0

        registry.enable("custom-extension")
        assert registry.is_enabled("custom-extension")
        assert len(registry.get_active_plugins()) == 1

        registry.disable("custom-extension")
        assert not registry.is_enabled("custom-extension")

    def test_priority_ordering(self):
        """Test that plugins are sorted by priority."""
        registry = PluginRegistry()

        low_priority = PostGenerationPlugin()  # priority 200
        high_priority = CustomExtensionPlugin()  # priority 50
        normal_priority = SchemaModifierPlugin()  # priority 100 (default)

        registry.register(low_priority)
        registry.register(high_priority)
        registry.register(normal_priority)

        active = registry.get_active_plugins()
        assert active[0].name == "custom-extension"  # priority 50
        assert active[1].name == "schema-modifier"  # priority 100
        assert active[2].name == "post-generation"  # priority 200

    def test_generation_count_increments(self):
        """Test that generation count increments on changes."""
        registry = PluginRegistry()
        initial_count = registry.generation_count

        plugin = CustomExtensionPlugin()
        registry.register(plugin)
        assert registry.generation_count == initial_count + 1

        registry.disable("custom-extension")
        assert registry.generation_count == initial_count + 2

        registry.enable("custom-extension")
        assert registry.generation_count == initial_count + 3

        registry.unregister("custom-extension")
        assert registry.generation_count == initial_count + 4

    def test_cache_invalidation_callback(self):
        """Test that cache invalidation callback is called."""
        callback_called = []

        def on_invalidate():
            callback_called.append(True)

        registry = PluginRegistry(on_cache_invalidation=on_invalidate)
        plugin = CustomExtensionPlugin()

        registry.register(plugin)
        assert len(callback_called) == 1

        registry.disable("custom-extension")
        assert len(callback_called) == 2


# =============================================================================
# Plugin Execution Tests
# =============================================================================


class TestPluginExecution:
    """Tests for plugin execution during schema generation."""

    def test_modify_operation_plugin(self):
        """Test that modify_operation hook is called."""
        plugin = CustomExtensionPlugin()
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[plugin],
        )

        @app.get("/items")
        def get_items():
            return []

        schema = app.openapi()

        # Check the custom extension was added
        operation = schema["paths"]["/items"]["get"]
        assert operation.get("x-custom-extension") is True
        assert operation.get("x-route-name") == "get_items"

    def test_modify_schema_plugin(self):
        """Test that modify_schema hook is called."""
        plugin = SchemaModifierPlugin()
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[plugin],
        )

        @app.get("/items")
        def get_items():
            return []

        schema = app.openapi()

        assert schema.get("x-generated-by") == "FastAPI Plugin System"
        assert schema["info"].get("x-plugin-version") == "1.0"

    def test_post_generation_plugin(self):
        """Test that post_schema_generation hook is called."""
        plugin = PostGenerationPlugin()
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[plugin],
        )

        @app.get("/items")
        def get_items():
            return []

        schema = app.openapi()

        assert schema.get("x-post-processed") is True

    def test_pre_schema_generation_plugin(self):
        """Test that pre_schema_generation hook is called."""
        plugin = PreSchemaPlugin()
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[plugin],
        )

        @app.get("/items")
        def get_items():
            return []

        schema = app.openapi()

        assert plugin.pre_called is True
        assert plugin.settings_received is not None
        assert plugin.settings_received.title == "Test API"
        assert plugin.settings_received.version == "1.0.0"

    def test_multiple_plugins(self):
        """Test multiple plugins working together."""
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[
                CustomExtensionPlugin(),
                SchemaModifierPlugin(),
                PostGenerationPlugin(),
            ],
        )

        @app.get("/items")
        def get_items():
            return []

        schema = app.openapi()

        # All plugins should have modified the schema
        operation = schema["paths"]["/items"]["get"]
        assert operation.get("x-custom-extension") is True
        assert schema.get("x-generated-by") == "FastAPI Plugin System"
        assert schema.get("x-post-processed") is True

    def test_plugin_error_handling(self):
        """Test that plugin errors don't break schema generation."""
        error_plugin = ErrorPlugin()
        normal_plugin = SchemaModifierPlugin()

        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[error_plugin, normal_plugin],
        )

        @app.get("/items")
        def get_items():
            return []

        # Should not raise, error is caught
        with pytest.warns(UserWarning, match="raised an error"):
            schema = app.openapi()

        # Normal plugin should still work
        assert schema.get("x-generated-by") == "FastAPI Plugin System"

    def test_plugin_cache_invalidation(self):
        """Test that schema is regenerated when plugins change."""
        app = FastAPI(
            title="Test API",
            version="1.0.0",
        )

        @app.get("/items")
        def get_items():
            return []

        # First generation - no plugins
        schema1 = app.openapi()
        assert schema1.get("x-generated-by") is None

        # Register a plugin
        app.openapi_plugins.register(SchemaModifierPlugin())

        # Should regenerate with plugin
        schema2 = app.openapi()
        assert schema2.get("x-generated-by") == "FastAPI Plugin System"

        # Disable plugin
        app.openapi_plugins.disable("schema-modifier")

        # Should regenerate without plugin effect
        schema3 = app.openapi()
        assert schema3.get("x-generated-by") is None


# =============================================================================
# create_plugin() Tests
# =============================================================================


class TestCreatePlugin:
    """Tests for the create_plugin convenience function."""

    def test_create_simple_plugin(self):
        """Test creating a plugin from callbacks."""
        plugin = create_plugin(
            "simple-plugin",
            modify_operation=lambda route, method, op: {**op, "x-simple": True},
        )

        assert plugin.name == "simple-plugin"
        assert plugin.priority == 100

        # Test the callback works
        result = plugin.modify_operation(None, "GET", {"summary": "Test"})
        assert result["x-simple"] is True
        assert result["summary"] == "Test"

    def test_create_plugin_with_priority(self):
        """Test creating a plugin with custom priority."""
        plugin = create_plugin(
            "priority-plugin",
            priority=25,
        )

        assert plugin.priority == 25


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests with actual HTTP requests."""

    def test_plugin_with_test_client(self):
        """Test plugin output via test client."""
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[CustomExtensionPlugin()],
        )

        @app.get("/items", response_model=list[Item])
        def get_items():
            return []

        @app.post("/items", response_model=Item)
        def create_item(item: Item):
            return item

        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()

        # Check both operations have custom extension
        assert schema["paths"]["/items"]["get"].get("x-custom-extension") is True
        assert schema["paths"]["/items"]["post"].get("x-custom-extension") is True

    def test_docs_with_plugins(self):
        """Test that Swagger UI still works with plugins."""
        app = FastAPI(
            title="Test API",
            version="1.0.0",
            openapi_plugins=[SchemaModifierPlugin()],
        )

        @app.get("/items")
        def get_items():
            return []

        client = TestClient(app)

        # Swagger UI should load
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger-ui" in response.text.lower()

        # ReDoc should load
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()
