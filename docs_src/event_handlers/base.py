import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Module-level registry populated by the @register_handler decorator.
HANDLERS: list[type["BaseEventHandler"]] = []


def register_handler(cls: type["BaseEventHandler"]) -> type["BaseEventHandler"]:
    """Register an event handler class in the global HANDLERS registry."""
    HANDLERS.append(cls)
    return cls


@dataclass
class BaseEventHandler(ABC):
    """Base class every event handler must inherit from."""

    event_name: str = ""

    @abstractmethod
    def handle(self, payload: dict) -> dict:
        """Process the incoming event payload and return a result."""
        ...

    @abstractmethod
    def validate(self, payload: dict) -> bool:
        """Return True when the payload is valid for this handler."""
        ...
