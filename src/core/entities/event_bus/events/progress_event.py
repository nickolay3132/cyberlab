from dataclasses import dataclass
from typing import Optional

from src.core.entities.event_bus import IEvent
from src.core.enums import DownloadingType

@dataclass
class ProgressEvent(IEvent):
    id: str
    type: DownloadingType
    total: int
    actual: int
    error_msg: Optional[str] = None