import time
from typing import List, Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


class SubModel(BaseModel):
    name: str
    value: int = 42


class MainModel(BaseModel):
    id: int
    title: str
    sub: SubModel
    items: List[SubModel]
    maybe: Optional[str] = None


def run_benchmark():
    sub = SubModel(name="test")
    model = MainModel(
        id=1,
        title="hello",
        sub=sub,
        items=[sub] * 50,  # 50 items to have a decent dictionary size
    )

    iterations = 20000
    print(f"Benchmarking jsonable_encoder over {iterations} iterations...")

    # 1. Optimized Path (Direct return)
    # Warmup
    for _ in range(100):
        jsonable_encoder(model)

    start_time = time.perf_counter()
    for _ in range(iterations):
        jsonable_encoder(model)
    optimized_time = time.perf_counter() - start_time

    # 2. Original Path (Double serialization via model_dump + recursive dict encoding)
    # Warmup
    for _ in range(100):
        jsonable_encoder(model.model_dump(mode="json"))

    start_time = time.perf_counter()
    for _ in range(iterations):
        # We simulate the exact old logic: model_dump(mode="json") followed by recursive jsonable_encoder
        obj_dict = model.model_dump(mode="json")
        jsonable_encoder(obj_dict)
    original_time = time.perf_counter() - start_time

    print(f"Original Code Path:  {original_time:.4f} seconds")
    print(f"Optimized Code Path: {optimized_time:.4f} seconds")
    print(f"Speedup: {original_time / optimized_time:.2f}x")


if __name__ == "__main__":
    run_benchmark()
