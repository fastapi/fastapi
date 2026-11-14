from typing import Literal

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
    contact: Person | Company = Form(discriminator="contact_type"),
    token: str = Form(),
    notification: Email | SMS | None = Form(
        default=None, discriminator="notification_type"
    ),
):
    return {"contact": contact, "notification": notification, "token": token}
