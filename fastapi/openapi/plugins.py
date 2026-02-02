"""OpenAPI plugin system for extending schema generation."""

import threading
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, Protocol, Union, runtime_checkable

if TYPE_CHECKING:
    from fastapi import FastAPI
    from fastapi.routing import APIRoute


@dataclass
class OpenAPIPluginSettings:
    """Settings passed to plugins during schema generation."""

    title: str
    version: str
    openapi_version: str
    description: Optional[str] = None
    routes_count: int = 0
    separate_input_output_schemas: bool = True


@runtime_checkable
class OpenAPIPlugin(Protocol):
    """Protocol defining the interface for OpenAPI plugins."""

    @property
    def name(self) -> str:
        """Unique identifier for the plugin."""
        ...

    @property
    def priority(self) -> int:
        """Execution priority. Lower numbers execute first. Default is 100."""
        ...

    def pre_schema_generation(
        self,
        app: "FastAPI",
        settings: OpenAPIPluginSettings,
    ) -> None:
        """Called before schema generation begins."""
        ...

    def modify_operation(
        self,
        route: "APIRoute",
        method: str,
        operation: dict[str, Any],
    ) -> dict[str, Any]:
        """Called for each operation. Returns the modified operation dict."""
        ...

    def modify_schema(
        self,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        """Called after base schema is built. Returns the modified schema."""
        ...

    def post_schema_generation(
        self,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        """Called as the final step. Returns the final schema."""
        ...


class OpenAPIPluginBase(ABC):
    """Abstract base class for OpenAPI plugins with default implementations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin identifier."""
        raise NotImplementedError

    @property
    def priority(self) -> int:
        """Execution priority. Override to change order."""
        return 100

    def pre_schema_generation(
        self,
        app: "FastAPI",
        settings: OpenAPIPluginSettings,
    ) -> None:
        pass

    def modify_operation(
        self,
        route: "APIRoute",
        method: str,
        operation: dict[str, Any],
    ) -> dict[str, Any]:
        return operation

    def modify_schema(
        self,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        return schema

    def post_schema_generation(
        self,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        return schema


@dataclass
class PluginState:
    """Internal state for a registered plugin."""

    plugin: Union[OpenAPIPlugin, OpenAPIPluginBase]
    enabled: bool = True
    error_count: int = 0
    last_error: Optional[Exception] = None


class PluginRegistry:
    """Thread-safe registry for managing OpenAPI plugins."""

    def __init__(
        self,
        *,
        max_errors_before_disable: int = 3,
        on_cache_invalidation: Optional[callable] = None,
    ) -> None:
        self._plugins: dict[str, PluginState] = {}
        self._lock = threading.RLock()
        self._max_errors = max_errors_before_disable
        self._cache_invalidation_callback = on_cache_invalidation
        self._generation_count = 0

    def register(
        self,
        plugin: Union[OpenAPIPlugin, OpenAPIPluginBase],
        *,
        enabled: bool = True,
        replace: bool = False,
    ) -> None:
        """Register a plugin. Raises ValueError if name exists and replace=False."""
        if not hasattr(plugin, "name"):
            raise TypeError(
                f"Plugin must have a 'name' property, got {type(plugin).__name__}"
            )

        name = plugin.name
        if not isinstance(name, str) or not name:
            raise ValueError(f"Plugin name must be a non-empty string, got {name!r}")

        with self._lock:
            if name in self._plugins and not replace:
                raise ValueError(
                    f"Plugin '{name}' is already registered. "
                    f"Use replace=True to override or unregister first."
                )
            self._plugins[name] = PluginState(plugin=plugin, enabled=enabled)
            self._invalidate_cache()

    def unregister(self, name: str) -> bool:
        """Remove a plugin. Returns True if removed, False if not found."""
        with self._lock:
            if name in self._plugins:
                del self._plugins[name]
                self._invalidate_cache()
                return True
            return False

    def enable(self, name: str) -> bool:
        """Enable a plugin. Returns True if enabled, False if not found."""
        with self._lock:
            if name in self._plugins:
                state = self._plugins[name]
                if not state.enabled:
                    state.enabled = True
                    state.error_count = 0
                    self._invalidate_cache()
                return True
            return False

    def disable(self, name: str) -> bool:
        """Disable a plugin. Returns True if disabled, False if not found."""
        with self._lock:
            if name in self._plugins:
                state = self._plugins[name]
                if state.enabled:
                    state.enabled = False
                    self._invalidate_cache()
                return True
            return False

    def is_enabled(self, name: str) -> bool:
        """Check if a plugin is enabled."""
        with self._lock:
            state = self._plugins.get(name)
            return state.enabled if state else False

    def get_plugin(
        self, name: str
    ) -> Optional[Union[OpenAPIPlugin, OpenAPIPluginBase]]:
        """Get a plugin by name."""
        with self._lock:
            state = self._plugins.get(name)
            return state.plugin if state else None

    def get_active_plugins(self) -> list[Union[OpenAPIPlugin, OpenAPIPluginBase]]:
        """Get all enabled plugins sorted by priority (lowest first)."""
        with self._lock:
            active = [
                state.plugin for state in self._plugins.values() if state.enabled
            ]
            return sorted(active, key=lambda p: getattr(p, "priority", 100))

    def get_all_plugins(
        self,
    ) -> dict[str, tuple[Union[OpenAPIPlugin, OpenAPIPluginBase], bool]]:
        """Get all plugins with their enabled status."""
        with self._lock:
            return {
                name: (state.plugin, state.enabled)
                for name, state in self._plugins.items()
            }

    def record_error(self, name: str, error: Exception) -> None:
        """Record an error. Auto-disables plugin after threshold."""
        with self._lock:
            state = self._plugins.get(name)
            if state:
                state.error_count += 1
                state.last_error = error
                if state.error_count >= self._max_errors:
                    warnings.warn(
                        f"OpenAPI plugin '{name}' auto-disabled after "
                        f"{state.error_count} errors. Last error: {error}",
                        stacklevel=2,
                    )
                    state.enabled = False
                    self._invalidate_cache()

    def clear(self) -> None:
        """Remove all plugins."""
        with self._lock:
            self._plugins.clear()
            self._invalidate_cache()

    @property
    def generation_count(self) -> int:
        """Counter incremented on cache invalidation."""
        return self._generation_count

    def _invalidate_cache(self) -> None:
        self._generation_count += 1
        if self._cache_invalidation_callback:
            try:
                self._cache_invalidation_callback()
            except Exception:
                pass

    def __len__(self) -> int:
        return len(self._plugins)

    def __contains__(self, name: str) -> bool:
        return name in self._plugins


class PluginExecutor:
    """Executes plugin hooks during schema generation."""

    def __init__(self, registry: PluginRegistry) -> None:
        self._registry = registry

    def execute_pre_schema_generation(
        self,
        app: "FastAPI",
        settings: OpenAPIPluginSettings,
    ) -> None:
        for plugin in self._registry.get_active_plugins():
            try:
                if hasattr(plugin, "pre_schema_generation"):
                    plugin.pre_schema_generation(app, settings)
            except Exception as e:
                self._handle_error(plugin, "pre_schema_generation", e)

    def execute_modify_operation(
        self,
        route: "APIRoute",
        method: str,
        operation: dict[str, Any],
    ) -> dict[str, Any]:
        result = operation
        for plugin in self._registry.get_active_plugins():
            try:
                if hasattr(plugin, "modify_operation"):
                    result = plugin.modify_operation(route, method, result)
                    if result is None:
                        result = operation
            except Exception as e:
                self._handle_error(plugin, "modify_operation", e)
        return result

    def execute_modify_schema(
        self,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        result = schema
        for plugin in self._registry.get_active_plugins():
            try:
                if hasattr(plugin, "modify_schema"):
                    result = plugin.modify_schema(result)
                    if result is None:
                        result = schema
            except Exception as e:
                self._handle_error(plugin, "modify_schema", e)
        return result

    def execute_post_schema_generation(
        self,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        result = schema
        for plugin in self._registry.get_active_plugins():
            try:
                if hasattr(plugin, "post_schema_generation"):
                    result = plugin.post_schema_generation(result)
                    if result is None:
                        result = schema
            except Exception as e:
                self._handle_error(plugin, "post_schema_generation", e)
        return result

    def _handle_error(self, plugin: Any, hook_name: str, error: Exception) -> None:
        plugin_name = getattr(plugin, "name", type(plugin).__name__)
        warnings.warn(
            f"OpenAPI plugin '{plugin_name}' raised an error in {hook_name}: {error}",
            stacklevel=3,
        )
        self._registry.record_error(plugin_name, error)


def create_plugin(
    name: str,
    *,
    priority: int = 100,
    pre_schema_generation: Optional[callable] = None,
    modify_operation: Optional[callable] = None,
    modify_schema: Optional[callable] = None,
    post_schema_generation: Optional[callable] = None,
) -> OpenAPIPluginBase:
    """Create a plugin from callback functions."""

    class CallbackPlugin(OpenAPIPluginBase):
        @property
        def name(self) -> str:
            return name

        @property
        def priority(self) -> int:
            return priority

    plugin = CallbackPlugin()

    if pre_schema_generation:
        plugin.pre_schema_generation = pre_schema_generation  # type: ignore
    if modify_operation:
        plugin.modify_operation = modify_operation  # type: ignore
    if modify_schema:
        plugin.modify_schema = modify_schema  # type: ignore
    if post_schema_generation:
        plugin.post_schema_generation = post_schema_generation  # type: ignore

    return plugin
