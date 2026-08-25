from typing import Annotated

from fastapi import Depends


async def dependency_a():
    dep_a = object()
    try:
        yield dep_a
    finally:
        if hasattr(dep_a, "close"):
            dep_a.close()


async def dependency_b(dep_a: Annotated[object, Depends(dependency_a)]):
    dep_b = object()
    try:
        yield dep_b
    finally:
        if hasattr(dep_b, "close"):
            # pass dep_a if the close method expects it
            try:
                dep_b.close(dep_a)
            except TypeError:
                dep_b.close()


async def dependency_c(dep_b: Annotated[object, Depends(dependency_b)]):
    dep_c = object()
    try:
        yield dep_c
    finally:
        if hasattr(dep_c, "close"):
            try:
                dep_c.close(dep_b)
            except TypeError:
                dep_c.close()
