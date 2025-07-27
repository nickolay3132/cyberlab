from dataclasses import dataclass
from enum import Enum

from src.core.entities.event_bus import Event


class StrEventTypes(Enum):
    TITLE = "title"
    TEXT = "text"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SPACE = "space"

@dataclass
class StrEvent(Event):
    id: str
    type: StrEventTypes
    data: str
