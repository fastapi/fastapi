import logging
from dataclasses import dataclass

from .base import BaseEventHandler, register_handler

logger = logging.getLogger(__name__)


@register_handler
@dataclass
class PaymentReceivedHandler(BaseEventHandler):
    event_name: str = "payment.received"

    def handle(self, payload: dict) -> dict:
        logger.info("Handling event %s", self.event_name)
        return {"status": "ok", "event": self.event_name, "amount": payload["amount"]}

    def validate(self, payload: dict) -> bool:
        return "amount" in payload
