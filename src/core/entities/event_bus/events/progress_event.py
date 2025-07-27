from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.core.entities.event_bus import Event


class ProgressEventTypes(Enum):
    INIT = 'init'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ERROR = 'error'

@dataclass
class ProgressEvent(Event):
    id: str
    type: ProgressEventTypes
    total: int = 0
    actual: int = 0
    error_message: Optional[str] = None
