import logging
from dataclasses import dataclass

from .base import BaseEventHandler, register_handler

logger = logging.getLogger(__name__)


@register_handler
@dataclass
class OrderPlacedHandler(BaseEventHandler):
    event_name: str = "order.placed"

    def handle(self, payload: dict) -> dict:
        logger.info("Handling event %s", self.event_name)
        return {"status": "ok", "event": self.event_name, "order_id": payload["order_id"]}

    def validate(self, payload: dict) -> bool:
        return "order_id" in payload
