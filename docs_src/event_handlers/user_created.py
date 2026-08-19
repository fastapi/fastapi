import logging
from dataclasses import dataclass

from .base import BaseEventHandler, register_handler

logger = logging.getLogger(__name__)


@register_handler
@dataclass
class UserCreatedHandler(BaseEventHandler):
    event_name: str = "user.created"

    def handle(self, payload: dict) -> dict:
        logger.info("Handling event %s", self.event_name)
        return {"status": "ok", "event": self.event_name, "user_id": payload["id"]}

    def validate(self, payload: dict) -> bool:
        return "id" in payload
