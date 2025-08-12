from dataclasses import dataclass
from typing import List, Callable

from src.core.entities import Snapshot
from src.core.entities.event_bus import IEvent


@dataclass
class SelectSnapshotEvent(IEvent):
    snapshots: List[Snapshot]
    callback: Callable[[Snapshot], None]