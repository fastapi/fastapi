from typing import Annotated, Literal

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Person(BaseModel):
    contact_type: Literal["person"]
    name: str


class Company(BaseModel):
    contact_type: Literal["company"]
    company_name: str


class Email(BaseModel):
    notification_type: Literal["email"]
    email: str


class SMS(BaseModel):
    notification_type: Literal["sms"]
    phone: str


@app.post("/contacts/")
async def create_contact(
    contact: Annotated[Person | Company, Form(discriminator="contact_type")],
    token: Annotated[str, Form()],
    notification: Annotated[
        Email | SMS | None, Form(discriminator="notification_type")
    ] = None,
):
    return {"contact": contact, "notification": notification, "token": token}
