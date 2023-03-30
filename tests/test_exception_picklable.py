from pickle import dumps, loads

from fastapi import HTTPException


def test_http_exception_is_picklable():
    exc = HTTPException(status_code=415)
    serialized_exc = dumps(exc)
    loads(serialized_exc)
