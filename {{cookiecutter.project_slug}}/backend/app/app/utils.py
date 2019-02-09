import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

import emails
import jwt
from emails.template import JinjaTemplate
from jwt.exceptions import InvalidTokenError

from app.core.config import (
    EMAIL_RESET_TOKEN_EXPIRE_HOURS,
    EMAIL_TEMPLATES_DIR,
    EMAILS_ENABLED,
    EMAILS_FROM_EMAIL,
    EMAILS_FROM_NAME,
    PROJECT_NAME,
    SECRET_KEY,
    SERVER_HOST,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_TLS,
    SMTP_USER,
)

password_reset_jwt_subject = "preset"


def send_email(email_to: str, subject_template="", html_template="", environment={}):
    assert EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(EMAILS_FROM_NAME, EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": SMTP_HOST, "port": SMTP_PORT}
    if SMTP_TLS:
        smtp_options["tls"] = True
    if SMTP_USER:
        smtp_options["user"] = SMTP_USER
    if SMTP_PASSWORD:
        smtp_options["password"] = SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str):
    subject = f"{PROJECT_NAME} - Test email"
    with open(Path(EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, username: str, token: str):
    subject = f"{PROJECT_NAME} - Password recovery for user {username}"
    with open(Path(EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    link = f"{SERVER_HOST}/reset-password?token={use_token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": PROJECT_NAME,
            "username": username,
            "email": email_to,
            "valid_hours": EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str):
    subject = f"{PROJECT_NAME} - New acccount for user {username}"
    with open(Path(EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = f"{SERVER_HOST}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(username):
    delta = timedelta(hours=EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "sub": password_reset_jwt_subject,
            "username": username,
        },
        SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token) -> Union[str, bool]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["username"]
    except InvalidTokenError:
        return False
