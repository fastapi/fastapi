from fastapi import Depends


async def dependency_a():
    class DBSession:
        def close(self, *args, **kwargs):
            pass
    dep_a = DBSession()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    class DBSession:
        def close(self, *args, **kwargs):
            pass
    dep_b = DBSession()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    class DBSession:
        def close(self, *args, **kwargs):
            pass
    dep_c = DBSession()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
