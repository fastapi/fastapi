"""
Benchmark: lazy allowed_keys allocation in jsonable_encoder.

Usage:
    uv run python scripts/bench_jsonable_encoder.py

Run against both branches to compare:
    git stash      # unpatched
    uv run python scripts/bench_jsonable_encoder.py
    git stash pop  # patched
    uv run python scripts/bench_jsonable_encoder.py

Reference results (20 rounds x 300 iters, mean, Python 3.12, FastAPI 0.136.1):

    Payload                               mean µs/call    stdev
    ------------------------------------------------------------
    small dict (3 keys)          before:      5.37µs      0.95
                                  after:      4.93µs      0.65   -8.2%
    large dict (300 items, nested)
                                 before:  12,158.80µs    557.40
                                  after:  11,431.07µs    506.29  -6.0%
"""

import statistics
import timeit
from typing import Any

from fastapi.encoders import jsonable_encoder

LARGE_ITEMS: list[dict[str, Any]] = [
    {
        "id": i,
        "name": f"item-{i}",
        "values": list(range(25)),
        "meta": {"active": True, "group": i % 10, "tag": f"t{i % 5}"},
    }
    for i in range(300)
]
LARGE_METADATA: dict[str, Any] = {
    "source": "benchmark",
    "version": 1,
    "flags": {"a": True, "b": False, "c": True},
    "notes": ["x" * 50, "y" * 50, "z" * 50],
}
LARGE_PAYLOAD: dict[str, Any] = {"items": LARGE_ITEMS, "metadata": LARGE_METADATA}
SMALL_PAYLOAD: dict[str, Any] = {"name": "foo", "value": 123}

ROUNDS = 20
ITERS = 300


def bench(payload: dict[str, Any]) -> tuple[float, float]:
    times = []
    for _ in range(ROUNDS):
        t = timeit.timeit(lambda: jsonable_encoder(payload), number=ITERS)
        times.append(t / ITERS * 1e6)
    return statistics.mean(times), statistics.stdev(times)


if __name__ == "__main__":
    print(f"{'Payload':<35} {'mean µs/call':>14} {'stdev':>8}")
    print("-" * 60)
    for label, payload in [
        ("small dict (3 keys)", SMALL_PAYLOAD),
        ("large dict (300 items, nested)", LARGE_PAYLOAD),
    ]:
        mean, sd = bench(payload)
        print(f"{label:<35} {mean:>12.2f}µs {sd:>6.2f}")
    print(f"\n({ROUNDS} rounds x {ITERS} iters each)")
