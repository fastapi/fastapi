import pytest
from fastapi import FastAPI

app = FastAPI()


def test_no_query_method():
    with pytest.raises(AttributeError):
        getattr(app, "query")


