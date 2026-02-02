"""OpenAPI schema generation profiling utilities."""

import functools
import threading
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class TimingEntry:
    """Single timing measurement entry."""

    name: str
    duration_ms: float
    call_count: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfilingStats:
    """Aggregated profiling statistics for a function."""

    name: str
    total_time_ms: float = 0.0
    call_count: int = 0
    min_time_ms: float = float("inf")
    max_time_ms: float = 0.0
    timings: list[float] = field(default_factory=list)

    @property
    def avg_time_ms(self) -> float:
        return self.total_time_ms / self.call_count if self.call_count > 0 else 0.0

    def add_timing(self, duration_ms: float) -> None:
        self.total_time_ms += duration_ms
        self.call_count += 1
        self.min_time_ms = min(self.min_time_ms, duration_ms)
        self.max_time_ms = max(self.max_time_ms, duration_ms)
        self.timings.append(duration_ms)


class OpenAPIProfiler:
    """Thread-safe profiler for OpenAPI schema generation."""

    def __init__(self) -> None:
        self._enabled = False
        self._stats: dict[str, ProfilingStats] = defaultdict(
            lambda: ProfilingStats(name="")
        )
        self._lock = threading.Lock()
        self._context_stack: list[str] = []
        self._start_time: Optional[float] = None

    def enable(self) -> None:
        """Enable profiling."""
        with self._lock:
            self._enabled = True
            self._start_time = time.perf_counter()

    def disable(self) -> None:
        """Disable profiling."""
        with self._lock:
            self._enabled = False

    def reset(self) -> None:
        """Reset all collected statistics."""
        with self._lock:
            self._stats.clear()
            self._context_stack.clear()
            self._start_time = None

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    def record(self, name: str, duration_ms: float) -> None:
        """Record a timing measurement."""
        if not self._enabled:
            return
        with self._lock:
            if name not in self._stats:
                self._stats[name] = ProfilingStats(name=name)
            self._stats[name].add_timing(duration_ms)

    @contextmanager
    def measure(self, name: str):
        """Context manager to measure execution time of a code block."""
        if not self._enabled:
            yield
            return

        start = time.perf_counter()
        try:
            yield
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self.record(name, duration_ms)

    def get_stats(self) -> dict[str, ProfilingStats]:
        """Get a copy of current statistics."""
        with self._lock:
            return dict(self._stats)

    def get_total_time_ms(self) -> float:
        """Get total elapsed time since profiling was enabled."""
        if self._start_time is None:
            return 0.0
        return (time.perf_counter() - self._start_time) * 1000

    def get_report(self) -> str:
        """Generate a human-readable profiling report."""
        stats = self.get_stats()
        if not stats:
            return "No profiling data collected."

        total_time = self.get_total_time_ms()
        lines = [
            "=" * 80,
            "OpenAPI Schema Generation Profiling Report",
            "=" * 80,
            f"Total elapsed time: {total_time:.2f}ms",
            "",
            f"{'Function':<45} {'Calls':>6} {'Total':>10} {'Avg':>10} {'%':>6}",
            "-" * 80,
        ]

        sorted_stats = sorted(
            stats.values(), key=lambda s: s.total_time_ms, reverse=True
        )

        for stat in sorted_stats:
            pct = (stat.total_time_ms / total_time * 100) if total_time > 0 else 0
            lines.append(
                f"{stat.name:<45} {stat.call_count:>6} "
                f"{stat.total_time_ms:>9.2f}ms {stat.avg_time_ms:>9.2f}ms {pct:>5.1f}%"
            )

        lines.append("=" * 80)
        return "\n".join(lines)

    def print_report(self) -> None:
        """Print the profiling report to stdout."""
        print(self.get_report())


# Global profiler instance
openapi_profiler = OpenAPIProfiler()


def profiled(name: Optional[str] = None) -> Callable[[F], F]:
    """Decorator to instrument a function for profiling."""

    def decorator(func: F) -> F:
        func_name = name or f"{func.__module__}.{func.__qualname__}"

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not openapi_profiler.is_enabled:
                return func(*args, **kwargs)

            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration_ms = (time.perf_counter() - start) * 1000
                openapi_profiler.record(func_name, duration_ms)

        return wrapper  # type: ignore[return-value]

    return decorator


class ProfilingContext:
    """Context manager for scoped profiling sessions."""

    def __init__(self, auto_print: bool = False) -> None:
        self._auto_print = auto_print
        self._profiler = openapi_profiler

    def __enter__(self) -> "ProfilingContext":
        self._profiler.reset()
        self._profiler.enable()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._profiler.disable()
        if self._auto_print:
            self.print_report()

    def get_stats(self) -> dict[str, ProfilingStats]:
        return self._profiler.get_stats()

    def get_report(self) -> str:
        return self._profiler.get_report()

    def print_report(self) -> None:
        self._profiler.print_report()

    def get_total_time_ms(self) -> float:
        return self._profiler.get_total_time_ms()
