# This is more or less a workaround to make Depends and Security hashable
# as other tools that use them depend on that
# Ref: https://github.com/fastapi/fastapi/pull/14320

from fastapi import Depends, Security


def dep():
    pass


def test_depends_hashable():
    dep()  # just for coverage
    d1 = Depends(dep)
    d2 = Depends(dep)
    d3 = Depends(dep, scope="function")
    d4 = Depends(dep, scope="function")

    s1 = Security(dep)
    s2 = Security(dep)

    assert hash(d1) == hash(d2)
    assert hash(s1) == hash(s2)
    assert hash(d1) != hash(d3)
    assert hash(d3) == hash(d4)
