from typing import Annotated, Literal

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Person(BaseModel):
    kind: Literal["person"]
    name: str


class Company(BaseModel):
    kind: Literal["company"]
    company_name: str


@app.post("/contacts/")
async def create_contact(
    contact: Annotated[Person | Company | None, Form(discriminator="kind")] = None,
):
    return contact
