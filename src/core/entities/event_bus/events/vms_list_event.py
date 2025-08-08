from dataclasses import dataclass
from typing import List

from src.core.entities.event_bus import IEvent


@dataclass
class VmsListEvent(IEvent):
    vms_names: List[str]