from dataclasses import dataclass

from src.core.entities.Snapshot import Snapshot
from src.core.entities.event_bus import Event


@dataclass
class SnapshotsTreeEvent(Event):
    id: str
    root_snapshot: Snapshot