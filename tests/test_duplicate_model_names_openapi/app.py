from fastapi import FastAPI

from tests.test_duplicate_model_names_openapi.a.model import User as UserA
from tests.test_duplicate_model_names_openapi.b.model import User as UserB
from tests.test_duplicate_model_names_openapi.c.model import User as UserC

app = FastAPI()


@app.get("/a", response_model=UserA)
def user_a(): ...


@app.get("/b", response_model=UserB)
def user_b(): ...


@app.get("/c", response_model=UserC)
def user_c(): ...
