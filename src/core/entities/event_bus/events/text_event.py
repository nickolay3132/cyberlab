from dataclasses import dataclass

from src.core.entities.event_bus import IEvent
from src.core.enums.events import TextEventType


@dataclass
class TextEvent(IEvent):
    id: str
    type: TextEventType
    text: str