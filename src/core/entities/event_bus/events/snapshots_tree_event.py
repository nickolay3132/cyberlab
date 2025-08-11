from dataclasses import dataclass
from typing import Optional

from src.core.entities import Snapshot
from src.core.entities.event_bus import IEvent


@dataclass
class SnapshotsTreeEvent(IEvent):
    root_snapshot: Optional[Snapshot]