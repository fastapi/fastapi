from fastapi.exceptions import HTTPException

def test_string_representation():
    exception = HTTPException(status_code=400, detail='detail exception')
    assert exception.__str__() == 'HTTPException(status_code: 400, detail: detail exception)'