import logging

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

logger = logging.getLogger(__name__)


def send_notification(email: str):
    try:
        write_notification(email)
    except Exception:
        logger.exception("Could not send the notification to %s", email)


def write_notification(email: str):
    with open("log.txt", mode="w") as email_file:
        email_file.write(f"notification for {email}")


@app.post("/send-notification/{email}")
async def send_notification_endpoint(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_notification, email)
    return {"message": "Notification sent in the background"}
