"""Benchmark: email.message.Message vs string-parsing for content-type detection."""

import email.message
import timeit

from fastapi.routing import _is_json_content_type

CONTENT_TYPES = [
    "application/json",
    "application/json; charset=utf-8",
    "application/geo+json",
    "application/vnd.api+json",
    "text/plain",
    "application/xml",
    "application/octet-stream",
    "multipart/form-data; boundary=----",
    "application/not-really-json",
    "application/geo+json-seq",
]

ITERATIONS = 100_000


def old_is_json(content_type: str) -> bool:
    """Original implementation using email.message.Message."""
    message = email.message.Message()
    message["content-type"] = content_type
    if message.get_content_maintype() == "application":
        subtype = message.get_content_subtype()
        if subtype == "json" or subtype.endswith("+json"):
            return True
    return False


def bench(func, label: str) -> float:
    def run():
        for ct in CONTENT_TYPES:
            func(ct)

    elapsed = timeit.timeit(run, number=ITERATIONS)
    ops = ITERATIONS * len(CONTENT_TYPES)
    rate = ops / elapsed
    print(f"  {label:30s}  {elapsed:8.3f}s  ({rate:,.0f} ops/s)")
    return elapsed


def main() -> None:
    # Verify both implementations agree on all inputs
    for ct in CONTENT_TYPES:
        assert old_is_json(ct) == _is_json_content_type(ct), (
            f"Mismatch on {ct!r}: old={old_is_json(ct)}, new={_is_json_content_type(ct)}"
        )

    print(
        f"\nBenchmark: {ITERATIONS:,} iterations x {len(CONTENT_TYPES)} content-types\n"
    )

    old_time = bench(old_is_json, "email.message (old)")
    new_time = bench(_is_json_content_type, "string parsing (new)")

    speedup = old_time / new_time
    pct = (1 - new_time / old_time) * 100

    print(f"\n  Speedup: {speedup:.1f}x faster  ({pct:.1f}% reduction in time)")


if __name__ == "__main__":
    main()
