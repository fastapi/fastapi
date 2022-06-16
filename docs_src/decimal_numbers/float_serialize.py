from decimal import Decimal

from fastapi import FastAPI
from fastapi.responses import SimpleJSONResponse
from pydantic import BaseModel


class IrrationalNumbers(BaseModel):
    pi: Decimal
    e: Decimal

    class Config:
        json_encoders = {Decimal: lambda d: d}


app = FastAPI()

num_model = IrrationalNumbers(
    pi=Decimal("3.14159265358979323846264338327950288"),
    e=Decimal("2.71828182845904523536028747135266249"),
)


@app.get("/", response_model=IrrationalNumbers, response_class=SimpleJSONResponse)
def numbers():
    return num_model
